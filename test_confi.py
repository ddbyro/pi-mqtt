import yaml
import time

config = yaml.full_load(open('./config.yaml'))

# rela
# num_relays = len(config['relays'].keys())
mqtt_set_topic = []
# mqtt_set_topic.append()
# for relay in config['relays']:
print(config['relays'][0]['pin'])


# for cfg in config:
#      print(cfg)