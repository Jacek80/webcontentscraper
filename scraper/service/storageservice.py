import os
from django.urls import reverse
from django.core.files.storage import default_storage
from .webscraperservice import WebScraperService


class StorageService():
    service = WebScraperService()

    def store_text(self, text, identifier):
        path = os.path.join(default_storage.base_location, str(identifier), 'text', 'web_content.txt')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding="utf-8") as file:
            file.write(text)
            file.close()

    def store_images(self, images, identifier):
        path = os.path.join(default_storage.base_location, str(identifier), 'images', 'null.bin')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        for image in images:
            image_body_response = self.service.make_request(image)
            image_name = image.split("/")[-1]
            path = os.path.join(default_storage.base_location, str(identifier), 'images', image_name)
            with open(path, 'wb') as file:
                file.write(image_body_response.content)
                file.close()

    def get_stored_content(self, identifier):
        path = os.path.join(default_storage.base_location, str(identifier), 'images')
        try:
            images_list = os.listdir(path)
        except FileNotFoundError:
            images_list = []

        path = os.path.join(default_storage.base_location, str(identifier), 'text')
        try:
            text_list = os.listdir(path)
        except FileNotFoundError:
            text_list = []

        for i, image in enumerate(images_list):
            download_url = reverse('download', args=(identifier, 'images', image))
            images_list[i] = download_url

        for i, text in enumerate(text_list):
            download_url = reverse('download', args=(identifier, 'text', text))
            text_list[i] = download_url

        response = {
            'images': images_list,
            'text': text_list
        }

        return response

    def download(self, *args, **kwargs):
        path = os.path.join(default_storage.base_location, kwargs['identifier'], kwargs['type'], kwargs['filename'])

        if kwargs['type'] == 'images':
            with open(path, 'rb') as file:
                content = file.read()
                file.close()
        else:
            with open(path, 'r', encoding="utf-8") as file:
                content = file.read()
                file.close()

        return content
