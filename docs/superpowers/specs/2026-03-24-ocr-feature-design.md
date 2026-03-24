# OCR Feature Design

**Date:** 2026-03-24
**Project:** Screenshot Manager
**Status:** Approved

## Overview

Add an OCR button to the Screenshot Manager toolbar that extracts text from the selected image,
copies it to the clipboard, and displays it in a modal text dialog.

## Requirements

- User selects an image in the file list and clicks the OCR button
- OCR runs on the entire image
- Extracted text is automatically copied to the clipboard
- Extracted text is shown in a modal dialog with a scrollable text box and a Close button
- If no text is detected, a warning messagebox is shown instead of the dialog
- If Tesseract is not installed, show a clear error message with install instructions
- If no file is selected, show a warning (consistent with Crop/Copy behavior)

## Implementation

### Dependencies

- Add `pytesseract==0.3.13` to `requirements.txt` (file already exists, all entries are pinned)
- `win32clipboard` is already available via `pywin32`, a pre-existing unlisted project dependency
- Tesseract binary installed separately by the user via the official Windows installer:
  `https://github.com/UB-Mannheim/tesseract/wiki`

### UI — Toolbar Button

- Add an `OCR` button in the toolbar at **column 7**
- Add the following `columnconfigure` calls to `button_frame` alongside the existing ones for columns 0-4.
  Columns 5 (Crop) and 6 (Copy) already have buttons but are missing `columnconfigure` — add all three retroactively:
  ```python
  button_frame.columnconfigure(5, weight=1)
  button_frame.columnconfigure(6, weight=1)
  button_frame.columnconfigure(7, weight=1)
  ```
- Button definition:
  ```python
  ocr_btn = tk.Button(button_frame, text="OCR",
                      command=self.ocr_image,
                      bg=self.colors['print'], fg='#000000',
                      **btn_style)
  ocr_btn.grid(row=0, column=7, padx=3, sticky=(tk.W, tk.E), ipady=8)
  ```
- Keyboard shortcut — bind in `__init__` after the existing `Ctrl+P` binding.
  On Windows Tkinter, `Ctrl+Shift` produces the uppercase character, so use capital `O`:
  ```python
  self.root.bind("<Control-Shift-O>", lambda e: self.ocr_image())
  ```

### `ocr_image()` method on `ScreenshotApp`

`pytesseract` and `win32clipboard` are both imported lazily inside the method, consistent with how
`win32clipboard` is already imported inside `copy_image()`. This avoids a hard crash on startup if
`pytesseract` is not installed.

```python
def ocr_image(self):
    selection = self.file_listbox.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a file to OCR")
        return

    filename = self.file_listbox.get(selection[0])
    filepath = os.path.join(self.screenshot_folder, filename)

    try:
        import pytesseract
        import win32clipboard
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        image = Image.open(filepath)
        text = pytesseract.image_to_string(image).strip()

        if not text:
            messagebox.showwarning("No Text Found", "No text could be extracted from the image.")
            return

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
        win32clipboard.CloseClipboard()

        OcrResultWindow(self.root, text, self.colors)
        self.status_var.set(f"OCR complete: {filename}")

    except ImportError:
        messagebox.showerror("Missing Dependency",
                             "pytesseract is not installed.\nRun: pip install pytesseract==0.3.13")
    except pytesseract.pytesseract.TesseractNotFoundError:
        messagebox.showerror("Tesseract Not Found",
                             "Tesseract OCR is not installed.\n"
                             "Download it from: https://github.com/UB-Mannheim/tesseract/wiki")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run OCR: {str(e)}")
        self.status_var.set("Error running OCR")
```

Note: clipboard errors are caught by the generic `except Exception` block and reported as
"Failed to run OCR". This is acceptable behaviour.

### `OcrResultWindow` class

Constructor signature: `OcrResultWindow(master, text, colors)`

Subclass `tk.Toplevel`, placed after `CropWindow` and before `ScreenshotApp` in the file.

```python
class OcrResultWindow(tk.Toplevel):
    def __init__(self, master, text, colors):
        super().__init__(master)
        self.title("OCR Result")
        self.geometry("600x400")
        self.grab_set()
        self.transient(master)
        self.configure(bg=colors['bg'])

        # Scrollable text area
        text_frame = tk.Frame(self, bg=colors['bg'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(text_frame, wrap=tk.WORD,
                              yscrollcommand=scrollbar.set,
                              bg=colors['canvas_bg'], fg=colors['fg'],
                              font=('Consolas', 11))
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)  # Make read-only after inserting text

        # Close button
        close_btn = tk.Button(self, text="Close", command=self.destroy,
                              bg=colors['delete'], fg='#000000',
                              font=('Consolas', 12, 'bold'),
                              relief=tk.FLAT, bd=0, cursor='hand2')
        close_btn.pack(fill=tk.X, padx=10, pady=(0, 10), ipady=5)
```

## Error Handling Summary

| Scenario | Exception | Behavior |
|---|---|---|
| No file selected | — | `messagebox.showwarning` |
| `pytesseract` not installed | `ImportError` | `messagebox.showerror` with pip install instruction |
| Tesseract binary not found | `TesseractNotFoundError` | `messagebox.showerror` with download URL |
| No text detected | — | `messagebox.showwarning("No Text Found")` |
| Other exception (incl. clipboard) | `Exception` | `messagebox.showerror` with exception message |

## Files Changed

- `screenshot_app.py`:
  - Add `OcrResultWindow` class (after `CropWindow`, before `ScreenshotApp`)
  - Add `ocr_image()` method to `ScreenshotApp` (with lazy imports inside)
  - Add OCR button at column 7 in toolbar
  - Add `columnconfigure(5, weight=1)`, `(6, weight=1)`, `(7, weight=1)` to `button_frame`
  - Bind `<Control-Shift-O>` in `__init__`
- `requirements.txt` — add `pytesseract==0.3.13`
