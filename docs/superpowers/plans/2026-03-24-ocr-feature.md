# OCR Feature Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an OCR button to the Screenshot Manager toolbar that extracts text from a selected image, copies it to the clipboard, and shows it in a modal dialog.

**Architecture:** `pytesseract` is imported lazily at the top of `ocr_image()` in its own try/except, before any other try block, so that `pytesseract.pytesseract.TesseractNotFoundError` is always a valid name when caught. `win32clipboard` is imported lazily inside the same method (same pattern as `copy_image()`). A new `OcrResultWindow` tk.Toplevel subclass displays the result. All changes are confined to `screenshot_app.py` and `requirements.txt`.

**Tech Stack:** Python, Tkinter, pytesseract, Pillow (already in use), win32clipboard (already in use via pywin32)

**Spec:** `docs/superpowers/specs/2026-03-24-ocr-feature-design.md`

---

## File Map

| File | Change |
|---|---|
| `requirements.txt` | Add `pytesseract==0.3.13` |
| `screenshot_app.py` | Add `OcrResultWindow` class at line ~216 (after `CropWindow`, before `ScreenshotApp`) |
| `screenshot_app.py` | Add `ocr_image()` method after `copy_image()` (~line 792) |
| `screenshot_app.py` | Add `columnconfigure(5,6,7)` and OCR button in `setup_gui()` (~line 401 / ~line 460) |
| `screenshot_app.py` | Add `Ctrl+Shift+O` binding in `__init__` (~line 272) |

**Note on pywin32:** `win32api` and `win32clipboard` are already used by the app (lines 29, 775) via `pywin32`, which is a pre-existing unlisted dependency not in `requirements.txt`. Adding `pywin32` to `requirements.txt` is out of scope for this feature.

---

## Task 1: Add pytesseract to requirements.txt

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Add the dependency**

Open `requirements.txt`. It currently contains:
```
Pillow==10.0.0
keyboard==0.13.5
pystray==0.19.4
pyinstaller==6.3.0
```

Add one line:
```
pytesseract==0.3.13
```

- [ ] **Step 2: Verify**

```bash
cat requirements.txt
```
Expected: 5 lines, last one is `pytesseract==0.3.13`

- [ ] **Step 3: Commit**

```bash
git add requirements.txt
git commit -m "chore: add pytesseract dependency"
```

---

## Task 2: Add OcrResultWindow class

**Files:**
- Modify: `screenshot_app.py` — insert after line 215 (blank line at end of `CropWindow`, before `class ScreenshotApp:`)

The class displays OCR text in a scrollable, read-only dialog. Pattern mirrors `CropWindow`.

- [ ] **Step 1: Insert OcrResultWindow class**

In `screenshot_app.py`, insert the following class between the end of `CropWindow` and the start of `class ScreenshotApp:` (around line 216):

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
        text_widget.config(state=tk.DISABLED)

        # Close button
        close_btn = tk.Button(self, text="Close", command=self.destroy,
                              bg=colors['delete'], fg='#000000',
                              font=('Consolas', 12, 'bold'),
                              relief=tk.FLAT, bd=0, cursor='hand2')
        close_btn.pack(fill=tk.X, padx=10, pady=(0, 10), ipady=5)
```

- [ ] **Step 2: Verify the file parses**

```bash
python -c "import ast; ast.parse(open('screenshot_app.py').read()); print('OK')"
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add screenshot_app.py
git commit -m "feat: add OcrResultWindow class"
```

---

## Task 3: Add ocr_image() method to ScreenshotApp

**Files:**
- Modify: `screenshot_app.py` — insert after the `copy_image()` method (~line 791, before `create_camera_icon`)

**Important — safe import ordering to avoid NameError:**
`pytesseract` must be imported in its own `try/except ImportError` block *before* the main try block. This ensures `pytesseract` is a bound name when Python evaluates `except pytesseract.pytesseract.TesseractNotFoundError:` in the second block. If both were in one try/except, a non-pytesseract exception raised before the import would cause Python to evaluate `pytesseract.pytesseract.TesseractNotFoundError` while `pytesseract` is still unbound, raising `NameError` instead of the intended handler.

- [ ] **Step 1: Insert ocr_image() method**

After the closing of `copy_image()` (the line `self.status_var.set("Error copying image")`), and before `create_camera_icon`, insert:

```python
    def ocr_image(self):
        """Extract text from the selected image using OCR"""
        # Import pytesseract first in its own block so it is bound before
        # TesseractNotFoundError is referenced in the except clause below.
        try:
            import pytesseract
        except ImportError:
            messagebox.showerror("Missing Dependency",
                                 "pytesseract is not installed.\nRun: pip install pytesseract==0.3.13")
            return

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a file to OCR")
            return

        filename = self.file_listbox.get(selection[0])
        filepath = os.path.join(self.screenshot_folder, filename)

        try:
            import win32clipboard

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

        except pytesseract.pytesseract.TesseractNotFoundError:
            messagebox.showerror("Tesseract Not Found",
                                 "Tesseract OCR is not installed.\n"
                                 "Download it from: https://github.com/UB-Mannheim/tesseract/wiki")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run OCR: {str(e)}")
            self.status_var.set("Error running OCR")
```

- [ ] **Step 2: Verify the file parses**

```bash
python -c "import ast; ast.parse(open('screenshot_app.py').read()); print('OK')"
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add screenshot_app.py
git commit -m "feat: add ocr_image() method to ScreenshotApp"
```

---

## Task 4: Add OCR button to toolbar and fix columnconfigure

**Files:**
- Modify: `screenshot_app.py` — `setup_gui()` method (~lines 397-460)

Two sub-changes in `setup_gui()`:
1. Add `columnconfigure(5, 6, 7)` — columns 5 (Crop) and 6 (Copy) already have buttons at lines 449-460 but were never given `columnconfigure` entries. This adds them retroactively alongside the new column 7 for OCR. Do **not** re-add the Crop or Copy buttons — they already exist.
2. Add the OCR button after the existing Copy button at column 6.

The OCR button intentionally uses `bg=self.colors['print']` (lavender `#b4befe`), the same color as the Print button. This is a deliberate choice per the spec — no new color key is being added.

- [ ] **Step 1: Add columnconfigure calls**

Find this block in `setup_gui()` (around lines 397-401):
```python
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)
        button_frame.columnconfigure(4, weight=1)
```

Add three more lines immediately after:
```python
        button_frame.columnconfigure(5, weight=1)
        button_frame.columnconfigure(6, weight=1)
        button_frame.columnconfigure(7, weight=1)
```

- [ ] **Step 2: Add OCR button**

Find the Copy button block (around lines 455-460):
```python
        copy_btn = tk.Button(button_frame, text="📋 Copy",
                            command=self.copy_image,
                            bg=self.colors['success'], fg='#000000',
                            **btn_style)
        copy_btn.grid(row=0, column=6, padx=3, sticky=(tk.W, tk.E), ipady=8)
```

Add the OCR button immediately after (column 7):
```python
        # OCR button — uses same color as Print button (intentional per spec)
        ocr_btn = tk.Button(button_frame, text="🔍 OCR",
                            command=self.ocr_image,
                            bg=self.colors['print'], fg='#000000',
                            **btn_style)
        ocr_btn.grid(row=0, column=7, padx=3, sticky=(tk.W, tk.E), ipady=8)
```

- [ ] **Step 3: Verify the file parses**

```bash
python -c "import ast; ast.parse(open('screenshot_app.py').read()); print('OK')"
```
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add screenshot_app.py
git commit -m "feat: add OCR button to toolbar"
```

---

## Task 5: Bind Ctrl+Shift+O keyboard shortcut

**Files:**
- Modify: `screenshot_app.py` — `__init__` method (~line 272)

- [ ] **Step 1: Add the binding**

Find this line in `__init__` (line ~272):
```python
        self.root.bind("<Control-p>", lambda event: self.print_file())
```

Add immediately after:
```python
        self.root.bind("<Control-Shift-O>", lambda event: self.ocr_image())
```

**Note:** Capital `O` is required. On Windows Tkinter, `Ctrl+Shift` produces the uppercase character, so `<Control-shift-o>` (lowercase) silently fails to bind.

- [ ] **Step 2: Verify the file parses**

```bash
python -c "import ast; ast.parse(open('screenshot_app.py').read()); print('OK')"
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add screenshot_app.py
git commit -m "feat: bind Ctrl+Shift+O to OCR"
```

---

## Task 6: Manual verification

The app has no automated test suite. Verify the feature manually.

**Prerequisites:**
- Tesseract installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`
- `pytesseract` installed: `pip install pytesseract==0.3.13`
- At least one screenshot with visible text in `C:\Screenshot\`

- [ ] **Step 1: Launch the app**

```bash
python screenshot_app.py
```
Expected: App opens. Toolbar now shows 8 buttons with `🔍 OCR` at the right end.

- [ ] **Step 2: OCR a screenshot with text**

Select a screenshot that contains text. Click `🔍 OCR`.
Expected:
- `OcrResultWindow` opens showing the extracted text in a scrollable read-only text box with a Close button
- Status bar shows `OCR complete: <filename>`
- Paste into Notepad (`Ctrl+V`) confirms the text is on the clipboard

- [ ] **Step 3: Test with image containing no text**

Select a screenshot with no text. Click `🔍 OCR`.
Expected: Warning dialog "No text could be extracted from the image."

- [ ] **Step 4: Test with no file selected**

Deselect all files (click blank area in list). Click `🔍 OCR`.
Expected: Warning dialog "Please select a file to OCR"

- [ ] **Step 5: Test keyboard shortcut**

Select a screenshot. Press `Ctrl+Shift+O`.
Expected: Same behaviour as clicking the OCR button.

- [ ] **Step 6: Final commit if any fixes were made during verification**

```bash
git add screenshot_app.py
git commit -m "fix: OCR verification fixes"
```
