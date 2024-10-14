import json
import os

class Config:
    def __init__(self):
        self.configs = {}
        self.load_all_configs()

    def load_config(self, config_name):
        file_path = f"configuration/{config_name}.json"
        with open(file_path, "r") as file:
            config = json.load(file)
        self.configs[config_name] = config

    def load_all_configs(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_files = os.listdir(current_dir)
        for config_file in config_files:
            if config_file.endswith(".json"):
                config_name = os.path.splitext(config_file)[0]
                self.load_config(config_name)

    def save_config(self, config_name):
        file_path = f"config/{config_name}.json"
        with open(file_path, "w") as file:
            json.dump(self.configs[config_name], file)

    def get_config(self, config_name):
        return self.configs.get(config_name)

    def update_config(self, config_name, new_config):
        self.configs[config_name] = new_config
        self.save_config(config_name)