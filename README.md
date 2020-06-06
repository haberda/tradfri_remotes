# tradfri_remotes
AppDaemon app to use Tradfri remotes

This AppDaemon app allows you to use button presses from an Ikea Tradfri remote that has been paired to a Zigbee hub that reveals the button presses as a sensor in Home Assistant. This notably works with zigbee2mqtt which allows you to pair the remote and receive remote presses as sensor state changes. This attempts to mimic the normal usage of the remotes as much as possible without actually binding the remote to the lights or devices. This has the advantage of being able to be used with more than just Zigbee lights, and can potentially be used for any light in Home Assistant.

Note: as of this release color bulbs are not supported. The toggle and dimming features should work, but colors will not change.

Example apps.yaml:

```
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
