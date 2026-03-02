import cv2
from pose_detector import PoseDetector
from exercises.pushup import PushUp

# Initialize detector and exercise
detector = PoseDetector()
exercise = PushUp()

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect pose
    image, results = detector.detect_pose(frame)
    landmarks = detector.get_landmarks(results)

    if landmarks:
        count, angle = exercise.update(landmarks)

        # Display rep count
        cv2.putText(image, f'Reps: {count}', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display angle (for debugging)
        cv2.putText(image, f'Angle: {int(angle)}', (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    cv2.imshow("Edge AI Gym", image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()