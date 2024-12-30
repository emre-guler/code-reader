import cv2
import pytesseract
import re
import pandas as pd

# Read student names from file
with open('students.txt', 'r', encoding='utf-8') as file:
    names = [line.strip() for line in file.readlines()]

# Open camera
cap = cv2.VideoCapture(0)

# Set camera resolution (640x480 recommended)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Regex pattern to recognize: S-###-###-####
pattern = r'[A-Z]-\d{3}-\d{3}-\d{4}'

# Set to store previously recognized codes
recognized_codes = set()

assignments = []  # Store code and name matches
current_index = 0  # Track the index of names

while True:
    # Get a new frame in each loop
    ret, frame = cap.read()

    # If frame was successfully captured
    if ret:
        # Perform OCR
        text = pytesseract.image_to_string(frame)

        # Find texts matching the pattern using regex
        matches = re.findall(pattern, text)

        # If matching text is found
        for match in matches:
            if match not in recognized_codes:  # If not previously recorded
                print("Recognized text:", match)

                # Save text to file
                with open("recognized_text.txt", "a", encoding='utf-8') as file:
                    file.write(match + "\n")

                # Add recognized code to set
                recognized_codes.add(match)

                # Match name with code
                if current_index < len(names):  # If names are not exhausted
                    assignments.append((names[current_index], match))
                    current_index += 1  # Increment index

                # Exit loop if desired number of codes are read
                if current_index >= len(names):
                    print("All codes have been read.")
                    break

        # Show camera feed on screen
        cv2.imshow('Camera Feed', frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Break loop if all codes are read
    if current_index >= len(names):
        break

# Release camera and windows
cap.release()
cv2.destroyAllWindows()

# Create DataFrame if matches were made
if assignments:
    df = pd.DataFrame(assignments, columns=['Name', 'Code'])

    # Save to Excel file
    df.to_excel('student_codes.xlsx', index=False)
    print("Excel file created: student_codes.xlsx")
else:
    print("No codes were read, Excel file could not be created.")
