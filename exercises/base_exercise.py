class BaseExercise:
    def __init__(self):
        self.counter = 0
        self.stage = None

    def update(self, landmarks):
        raise NotImplementedError("Each exercise must implement update method")