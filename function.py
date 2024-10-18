import json
import os

import toml


class Helper:
    def __init__(self, path_to_json=None, path_to_toml=None):
        if path_to_json is None:
            tmp_path_to_json = os.path.dirname(os.path.realpath(__file__)) + "/data.json"
        
        if path_to_toml is None:
            tmp_path_to_toml = os.path.dirname(os.path.realpath(__file__)) + "/config.toml"

        self.path_to_json = tmp_path_to_json
        self.path_to_toml = tmp_path_to_toml

        if not os.path.isfile(self.path_to_json):
            with open("data.json", "w") as file:
                file.write("{}")
        

    def get_json(self) -> dict:
        with open(self.path_to_json, 'r') as file:
            answer = json.load(file)

        return answer

    
    def get_toml(self) -> dict:
        return toml.load(self.path_to_toml)
    
    def set_json(self, data) -> None:
        with open(self.path_to_json, 'w') as file:
            json.dump(data, file)
