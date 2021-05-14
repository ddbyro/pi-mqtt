import yaml
import time

config = yaml.full_load(open('./config.yaml'))

# rela
# num_relays = len(config['relays'].keys())
for relay in config['relays']:
    time.sleep(1)
    name = relay['name']
    pin = relay['pin']
    set_topic = relay['set_topic']
    status_topic = relay['status_topic']
    print(f'relay {name} is on pin {pin}, its topics are {set_topic} and {status_topic}')
# print(config['relays'][f'relay0{num_relays}'])

# for cfg in config:
#      print(cfg)