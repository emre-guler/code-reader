# Code Reader

A Python application that uses computer vision and OCR (Optical Character Recognition) to read and process specific code patterns from a camera feed. The application matches these codes with student names and exports the results to an Excel file.

## Features

- Real-time camera feed processing
- OCR text recognition using Tesseract
- Pattern matching using regex (format: S-###-###-####)
- Automatic student name and code matching
- Excel export functionality

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- Pytesseract
- Pandas
- Tesseract OCR engine

## Installation

1. Install the required Python packages:
```bash
pip install opencv-python pytesseract pandas openpyxl
```

2. Install Tesseract OCR engine:
   - For macOS: `brew install tesseract`
   - For Windows: Download and install from [GitHub Tesseract Release](https://github.com/UB-Mannheim/tesseract/wiki)
   - For Linux: `sudo apt-get install tesseract-ocr`

## Usage

1. Create a `students.txt` file with student names (one name per line)
2. Run the application:
```bash
python app.py
```
3. Point your camera at the codes you want to scan
4. Press 'q' to quit the application
5. Check the generated `student_codes.xlsx` file for results

## File Structure

- `app.py`: Main application code
- `students.txt`: Input file containing student names
- `student_codes.xlsx`: Output Excel file with matched names and codes
- `recognized_text.txt`: Log file of recognized codes

> **Note**: This project was generated with the assistance of AI (Cursor) to create a code reader application for processing student identification codes using OCR technology.

## License

This project is licensed under the terms specified in the LICENSE file. 