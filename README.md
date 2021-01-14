# Tradfri remotes
AppDaemon app to use Tradfri remotes for ZHA and Zigbee2MQTT

This AppDaemon app allows you to use button presses from an Ikea Tradfri remote that has been paired to a ZHA or Zigbee2MQTT hub. This attempts to mimic the normal usage of the remotes as much as possible without actually binding the remote to the lights. This has the advantage of being able to be used with more than just Zigbee lights, and can potentially be used for any light in Home Assistant.

Note: as of this release color bulbs are supported but an attempt is made to match them to color temperature rather than colors. Only lights are supported, other devices are not.

## Options:
---

Key | Required | Description | Default | Unit
------------ | ------------- | ------------- | ------------- | -------------
lights | True | List of lights | None | List
sensor | True if no ieee | list of remote sensors for Zigbee2MQTT | None | list
device_ieee | True if no sensors | list of remote ieee for ZHA | None | list
prefer_rgb | False | Always use RGB for supported lights | True | Boolean
min_kelvin | False | Minimum light temperature in Kelvin | 2200 | Kelvin
max_kelvin | False | Maximum light temperature in Kelvin | 5000 | Kelvin
brightness_step | False | How much to change the light brightness with each step | 25 | bit


## Supported remotes:

https://www.zigbee2mqtt.io/devices/E1524_E1810.html

https://www.zigbee2mqtt.io/devices/ICTC-G-1.html

## Example apps.yaml

```
#Example ZHA config with full suite of options
living_room_tradfri_remotes:
  module: tradfri_remotes
  class: tradfri_remotes
  lights:
    - light.living_room_lamp
    - light.living_room_lamp_2
    - light.living_room_dimmer
  device_ieee:
    - 00:0b:57:ff:fe:32:5f:ca
  prefer_rgb: True
  brightness_step: 25
  min_kelvin: 2200
  max_kelvin: 5000
    
#Example Zigbee2MQTT config with minimum set of options
kitchen_tradfri_remotes:
  module: tradfri_remotes
  class: tradfri_remotes
  lights:
    - light.kitchen_spotlight
    - light.main_cabinets
    - light.coffee_bar
    - light.kitchen_spotlight_left
    - light.kitchen_spotlight_right
  sensors:
    - sensor.tradfri_kitchen_remote
    - sensor.tradfri_kitchen_dimmer_action
    
```
