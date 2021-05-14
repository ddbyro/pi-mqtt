import yaml
# import RPiSim.GPIO as GPIO

config = yaml.full_load(open('./config.yaml'))
print(config['relays'])
#
# # rela
# # num_relays = len(config['relays'].keys())
# mqtt_set_topic = []
# # mqtt_set_topic.append()
# # for relay in config['relays']:
# gpio_pins = []
#
# for relay in config['relays']:
#     gpio_pins.append(relay['pin'])
#     mqtt_status_topic = relay['status_topic']
# for pin in gpio_pins:
#     print(gpio_pins)
#     re


# for cfg in config:
#      print(cfg)