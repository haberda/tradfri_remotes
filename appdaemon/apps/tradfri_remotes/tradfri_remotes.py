import hassapi as hass

class tradfri_remotes(hass.Hass):
    def initialize(self):
        self.sensors = self.args.get('sensors', None)
        self.lights = self.args.get('lights', None)
        if self.lights is not None and self.sensors is not None:
            if isinstance(self.lights, str):
                self.lights = self.lights.split(',')
            if isinstance(self.sensors, str):
                self.sensors = self.sensors.split(',')
            for sensor in self.sensors:
                self.listen_state(self.state_change, sensor)
        else:
            self.log('Either no lights or no sensors defined. Exiting.')
    def state_change(self, sensor, attribute, old, new, kwargs):
        for light in self.lights:
            if new == 'toggle':
                self.toggle(light)
            elif new == 'brightness_up_click':
                brightness = self.get_state(light, attribute = 'brightness')
                if brightness is not None:
                    if brightness < 255:
                        brightness += 10
                        if brightness > 255:
                            brightness = 255
                    self.turn_on(entity_id = light, brightness = brightness)
            elif new == 'brightness_down_click':
                brightness = self.get_state(light, attribute="brightness")
                if brightness is not None:
                    if brightness > 10:
                        brightness -= 10
                    self.turn_on(entity_id = light, brightness = brightness)
            elif new == 'arrow_right_click':
                color_temp = self.get_state(light, attribute="color_temp")
                if color_temp is not None:
                    if color_temp > 250:
                        color_temp -= 10
                    else:
                        color_temp = 500
                    self.turn_on(entity_id = light, color_temp = color_temp)
                else:
                    kelvin = self.get_state(light, attribute="kelvin")
                    if kelvin is not None:
                        if kelvin < 4000:
                            kelvin += 100
                        else:
                            kelvin = 2000
                        self.turn_on(entity_id = light, kelvin = kelvin)
            elif new == 'arrow_left_click':
                color_temp = self.get_state(light, attribute="color_temp")
                if color_temp is not None:
                    if color_temp < 500:
                        color_temp += 10
                    else:
                        color_temp = 250
                    self.turn_on(entity_id = light, color_temp = color_temp)
                else:
                    kelvin = self.get_state(light, attribute="kelvin")
                    if kelvin is not None:
                        if kelvin > 2000:
                            kelvin -= 100
                        else:
                            kelvin = 4000
                        self.turn_on(entity_id = light, kelvin = kelvin)
            elif new == 'rotate_stop':
                brightness = self.get_state(sensor, attribute="brightness")
                if brightness is not None:
                    self.turn_on(entity_id = light, brightness = brightness)
