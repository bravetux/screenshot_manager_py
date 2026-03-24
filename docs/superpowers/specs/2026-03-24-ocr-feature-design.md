# OCR Feature Design

**Date:** 2026-03-24
**Project:** Screenshot Manager
**Status:** Approved

## Overview

Add an OCR button to the Screenshot Manager toolbar that extracts text from the selected image, copies it to the clipboard, and displays it in a modal text dialog.

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

- Add `pytesseract` to `requirements.txt`
- Tesseract binary installed separately by the user via the official Windows installer

### UI

- Add a `OCR` button in the toolbar at column 7, same style as existing buttons
- Button triggers `self.ocr_image()` method on `ScreenshotApp`

### `ocr_image()` method on `ScreenshotApp`

1. Check for a selected file; if none, show warning and return
2. Open the image with Pillow
3. Call `pytesseract.image_to_string(image)`
4. If result is empty/whitespace, show a warning messagebox and return
5. Copy result to clipboard via `win32clipboard`
6. Open `OcrResultWindow` modal dialog with the extracted text

### `OcrResultWindow` (new `tk.Toplevel` class)

- Modal (`grab_set`, `transient`)
- Title: "OCR Result"
- Contains a scrollable `Text` widget (read-only) displaying the extracted text
- A `Close` button at the bottom
- Styled with the app's `colors` dict, consistent with `CropWindow`

### Error Handling

| Scenario | Behavior |
|---|---|
| No file selected | `messagebox.showwarning` |
| Tesseract not installed | `messagebox.showerror` with install link |
| No text detected | `messagebox.showwarning("No text found")` |
| Other exception | `messagebox.showerror` with exception message |

## Files Changed

- `screenshot_app.py` — add `OcrResultWindow` class and `ocr_image()` method, add OCR button to toolbar
- `requirements.txt` — add `pytesseract`
