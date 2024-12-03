import cv2, numpy as np, sys

cap = cv2.VideoCapture(0)
print('Setting up background. Please move out of frame.')
ret, frame = cap.read()
if not ret:
    print('Error: Could not capture background.')
    cap.release()
    sys.exit()

average_background = np.float32(frame)
for i in range(1, 36):
    ret, frame = cap.read()
    if not ret:
        print(f'Error: Could not read frame {i}')
        continue
    cv2.accumulateWeighted(frame, average_background, alpha=1.0/i)
background = cv2.convertScaleAbs(average_background)

print("Starting main loop. Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        continue
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    mask = ((hsv[..., 0] >= lower_blue[0]) & (hsv[..., 0] <= upper_blue[0]) &  
            (hsv[..., 1] >= lower_blue[1]) & (hsv[..., 1] <= upper_blue[1]) &  
            (hsv[..., 2] >= lower_blue[2]) & (hsv[..., 2] <= upper_blue[2])).astype(np.uint8) * 255

    mask_3d = np.stack([mask] * 3, axis=-1) // 255  
    background_area = background * mask_3d  
    foreground_area = frame * (1 - mask_3d)  
    result = background_area + foreground_area
    cv2.imshow('Invisible Cloak', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

    