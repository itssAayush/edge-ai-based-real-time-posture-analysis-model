from angle_utils import calculate_angle
from exercises.base_exercise import BaseExercise
import numpy as np


class PushUp(BaseExercise):

    def __init__(self):
        super().__init__()

        self.angle_history = []
        self.direction = None
        self.bottom_reached = False
        self.cooldown = 0

    def smooth_angle(self, angle):
        self.angle_history.append(angle)

        if len(self.angle_history) > 5:
            self.angle_history.pop(0)

        return np.mean(self.angle_history)

    def body_is_horizontal(self, landmarks):
        shoulder_y = landmarks[11].y
        hip_y = landmarks[23].y

        # If shoulder and hip are close vertically → body horizontal
        return abs(shoulder_y - hip_y) < 0.1

    def update(self, landmarks):

        shoulder = [landmarks[11].x, landmarks[11].y]
        elbow = [landmarks[13].x, landmarks[13].y]
        wrist = [landmarks[15].x, landmarks[15].y]

        raw_angle = calculate_angle(shoulder, elbow, wrist)
        angle = self.smooth_angle(raw_angle)

        # Cooldown to avoid double count
        if self.cooldown > 0:
            self.cooldown -= 1
            return self.counter, angle

        # Ignore if body not horizontal
        if not self.body_is_horizontal(landmarks):
            return self.counter, angle

        # Detect movement direction
        if len(self.angle_history) >= 2:
            if self.angle_history[-1] < self.angle_history[-2]:
                self.direction = "down"
            elif self.angle_history[-1] > self.angle_history[-2]:
                self.direction = "up"

        # Bottom position detection
        if angle < 70 and self.direction == "down":
            self.bottom_reached = True

        # Count rep when returning up after bottom
        if angle > 170 and self.bottom_reached and self.direction == "up":
            self.counter += 1
            self.bottom_reached = False
            self.cooldown = 15

        return self.counter, angle