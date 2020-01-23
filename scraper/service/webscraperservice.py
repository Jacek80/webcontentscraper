import requests
from ..exceptions import ServiceUnavailableException
from ..dictionaries import NO_SERVICE
from .textservice import TextService


class WebScraperService():
    def make_request(self, full_address):
        try:
            response = requests.get(full_address)
        except Exception as exc:
            raise ServiceUnavailableException(NO_SERVICE)

        return response

    def scrape_content(self, address):
        full_address = address if 'http' in address else 'http://' + address

        service_response = self.make_request(full_address)
        response_text = service_response.text

        images = TextService.get_images_from_text(response_text)
        text = TextService.clear_text(response_text)

        '''
        relative image paths hack
        '''
        if images:
            for i, image in enumerate(images):
                if 'http' not in image:
                    images[i] = full_address + image

        response = {
            'images': images,
            'text': text
        }

        return response



