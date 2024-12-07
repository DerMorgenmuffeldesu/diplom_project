from celery import shared_task
from PIL import Image
import os

@shared_task
def process_avatar(image_path, sizes):
    for size in sizes:
        with Image.open(image_path) as img:
            img.thumbnail(size)
            output_path = f"{image_path.rsplit('.', 1)[0]}_{size[0]}x{size[1]}.jpg"
            img.save(output_path)

def resize_image(image_path, size):
    with Image.open(image_path) as img:
        img.thumbnail(size)
        img.save(image_path)
