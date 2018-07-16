import yaml

def get_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

