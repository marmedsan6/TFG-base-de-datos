import requests

class PlantID:
    def __init__(self, api_key):
        self.api_key = api_key
        self.identify_url = "https://plant.id/api/v3/identification"

    def identify_plant(self, image_base64):
        headers = {
            "Content-Type": "application/json",
            "Api-Key": self.api_key
        }
        data = {
            "images": [image_base64]
        }

        response = requests.post(self.identify_url, json=data, headers=headers)
        response.raise_for_status() 

        return response.json()
