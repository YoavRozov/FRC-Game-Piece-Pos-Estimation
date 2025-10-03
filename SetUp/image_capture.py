import cv2

# =------ Configure these variables ------=
# Camera index, change this if you have multiple cameras connected
CAMERA_INDEX = 0

# Output image path
OUTPUT_IMAGE_PATH = "SetUp"

# Resolution
FRAME_WIDTH = 1280
FRAME_HEIGHT = 960
# =---------------------------------------=

# Initialize camera
cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

i = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key % 256 == 27:  # ESC pressed
        print("Escape hit, closing...")
        break
    elif key % 256 == ord('q'):  # 'q' pressed
        print("Quit hit, closing...")
        break
    elif key % 256 == 32:  # SPACE pressed
        img_name = f"{OUTPUT_IMAGE_PATH}/calibration_image_{i}.png"
        i += 1
        cv2.imwrite(img_name, frame)
        print(f"Image saved as {img_name}")

cap.release()
cv2.destroyAllWindows()