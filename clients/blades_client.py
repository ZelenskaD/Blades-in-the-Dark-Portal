import requests


class BladesClient:
    def __init__(self, config):
        self.url = config.API_URL

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



