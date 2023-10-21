import yaml

# Define a function to load the configuration file
def load_config(config_file_path: str):
    with open(config_file_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(f"Error reading the YAML file: {exc}")
            return None