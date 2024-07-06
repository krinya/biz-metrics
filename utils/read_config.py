import yaml

def read_config(config_file='config.yaml', section = 'all'):
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    if section != 'all':
        config = config[section]
    return config