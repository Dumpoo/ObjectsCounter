from imageai.Detection import ObjectDetection
from PIL import ImageOps, Image
import os


def calculate(project_path, image_path, crop_coords, screen_size, debug):
    image = Image.open(image_path)
    image = image.resize(screen_size)

    crop = ImageOps.crop(image, crop_coords)

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(project_path, 'static/model/yolo.h5'))
    detector.loadModel()
    detect = detector.detectObjectsFromImage(
        input_image=crop,
        input_type='array',
        output_type='array',
        display_object_name=False,
        display_percentage_probability=False
    )

    detection_name = detect[1][0]['name']
    custom = detector.CustomObjects()
    custom[detection_name] = 'valid'

    detect_all_objects = detector.detectObjectsFromImage(
        custom_objects=custom,
        input_type='array',
        input_image=image,
        output_type='array',
        thread_safe=True,
        display_object_name=debug,
        display_percentage_probability=debug
    )

    result = Image.fromarray(detect_all_objects[0], 'RGB')

    return len(detect_all_objects[1]), result
