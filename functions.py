import yaml
import re


def read_in_yaml_file(yaml_file):
    "Read in a yaml file as a dictionary"
    with open(yaml_file, 'r') as tmp_data:
        yaml_data = tmp_data.read()
    y = yaml.safe_load(yaml_data)
    return y


def get_ip(input):
    "Give it a patch of text, it returns a list of all IP addresses in that list"
    return(re.findall(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', input))
