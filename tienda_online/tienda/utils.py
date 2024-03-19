from django.core.files.storage import default_storage
from .interfaces import ImageStorage  

class ImageLocalStorage(ImageStorage):
    def store(self, image):
        if image:
            file_name = default_storage.save('uploads/product/' + image.name, image)
            return file_name