import requests


class BladesClient:
    def __init__(self, config):
        self.url = config.API_URL
        self.token = config.API_TOKEN

    def get_playbooks(self):
        response = requests.get(f"{self.url}/api/playbooks")
        if response.status_code != 200:
            return None
        else:
            return response.json()['details']['playbooks']

    def get_playbook(self, playbook_name):
        response = requests.get(f"{self.url}/api/playbooks/{playbook_name}")
        if response.status_code != 200:
            return None
        else:
            return response.json()['details']

    def get_character_skills(self, playbook_name):
        response = requests.get(f'{self.url}/api/playbooks/{playbook_name}')
        if response.status_code != 200:
            return None
        else:
            return response.json()['details']['attributes']

    def generate_image(self, character_id, look):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        data = {
            "characterId": f"{character_id}",
            "prompt": look
        }

        response = requests.post(f'{self.url}/api/ai/generate-character-image', json=data, headers=headers)

        print(f"Received response with status code: {response.status_code}")
        if response.status_code != 200:
            try:
                error_response = response.json()
                print(f"Error response: {error_response}")
            except ValueError:
                print("Failed to parse error response as JSON.")
                print(f"Raw error response: {response.text}")
            return None
        else:
            try:
                success_response = response.json()
                print(f"Success response: {success_response}")
                return success_response['details']['url']
            except ValueError:
                print("Failed to parse success response as JSON.")
                print(f"Raw success response: {response.text}")
                return None
