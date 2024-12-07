from celery import shared_task
from PIL import Image
import os


@shared_task
def process_product_image(image_path, sizes):
    """
    Создаёт миниатюры изображения заданных размеров.
    """
    for size in sizes:
        width, height = size
        img = Image.open(image_path)
        img = img.resize((width, height), Image.ANTIALIAS)

        # Создаём папку для миниатюр, если её нет
        base_dir = os.path.dirname(image_path)
        thumbnails_dir = os.path.join(base_dir, "thumbnails")
        os.makedirs(thumbnails_dir, exist_ok=True)

        # Сохраняем миниатюру
        thumbnail_path = os.path.join(thumbnails_dir, f"{width}x{height}_{os.path.basename(image_path)}")
        img.save(thumbnail_path)
        print(f"Thumbnail saved at: {thumbnail_path}")