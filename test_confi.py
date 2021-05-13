import yaml


config = yaml.full_load(open('./config.yaml'))


# print(config)
for config, relays in config.items():

     print(relays)