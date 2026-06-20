from ultralytics import YOLO  # type: ignore[import]


class FoodDetector:

    def __init__(self,
                 model_path="yolov8n.pt"):

        self.model = YOLO(model_path)

    def detect(self, image_path):

        results = self.model(image_path)

        foods = []

        for result in results:

            names = result.names

            for cls in result.boxes.cls:

                food = names[int(cls)]

                foods.append(food)

        return list(set(foods))