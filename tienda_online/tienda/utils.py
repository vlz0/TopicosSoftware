from django.core.files.storage import default_storage
from .interfaces import ImageStorage  
import requests
class ImageLocalStorage(ImageStorage):
    def store(self, image):
        if image:
            file_name = default_storage.save('uploads/product/' + image.name, image)
            return file_name 



def get_allied_brands():
    api_url = "https://run.mocky.io/v3/12470a11-9dfd-417e-bcc1-a85ff02d61ce"  
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
