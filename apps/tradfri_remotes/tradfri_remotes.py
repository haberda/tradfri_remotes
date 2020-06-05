import hassapi as hass
import datetime
from datetime import timedelta

class tradfri_remotes(hass.Hass):
    def initialize(self):
        self.sensors = self.args.get('sensors', None)
        self.lights = self.args.get('lights', None)
        self.service_data = {"entity_id": None}
        self.bu_handler = None
        self.bd_handler = None
        self.la_handler = None
        self.ra_handler = None
        if self.lights is not None and self.sensors is not None:
            if isinstance(self.lights, str):
                self.lights = self.lights.split(',')
            self.service_data['entity_id'] = self.lights
            if isinstance(self.sensors, str):
                self.sensors = self.sensors.split(',')
            for sensor in self.sensors:
                self.listen_state(self.state_change, sensor)
        else:
            self.log('Either no lights or no sensors defined. Exiting.')

    def mean_vals (self):
        color_temp = 0
        brightness = 0
        i=0
        j=0
        for light in self.lights:
            if self.get_state(light) == 'on':
                brightness_temp = self.get_state(light, attribute="brightness")
                if brightness_temp is not None:
                    i=i+1
                    brightness = brightness + self.get_state(light, attribute="brightness")
                color_temp_temp = self.get_state(light, attribute="color_temp")
                if color_temp_temp is not None:
                    j=j+1
                    color_temp = color_temp + self.get_state(light, attribute="color_temp")
        if brightness == 0:
            mean_brightness = 255
        else:
            mean_brightness = brightness / i
        if color_temp != 0:
            mean_color_temp = color_temp / j
        else:
            mean_color_temp = 0
        return mean_brightness, mean_color_temp

    def brightness_up_hold (self,kwargs):
        mean_brightness, mean_color_temp = self.mean_vals()
        service_data = self.service_data.copy()
        service_call = "light/turn_on"
        if mean_brightness < 245:
            service_data['brightness_step'] = 10
        else:
            service_data['brightness'] = 10
        self.call_service(service_call, **service_data)

    def brightness_down_hold (self,kwargs):
        mean_brightness, mean_color_temp = self.mean_vals()
        service_data = self.service_data.copy()
        service_call = "light/turn_on"
        if mean_brightness > 10:
            service_data['brightness_step'] = -10
        else:
            service_data['brightness'] = 255
        self.call_service(service_call, **service_data)

    def arrow_right_hold (self,kwargs):
        mean_brightness, mean_color_temp = self.mean_vals()
        service_data = self.service_data.copy()
        service_call = "light/turn_on"
        if mean_color_temp > 250:
            service_data['color_temp'] = mean_color_temp - 10
        else:
            service_data['color_temp'] = 500
        self.call_service(service_call, **service_data)

    def arrow_left_hold (self,kwargs):
        mean_brightness, mean_color_temp = self.mean_vals()
        service_data = self.service_data.copy()
        service_call = "light/turn_on"
        if mean_color_temp < 500:
            service_data['color_temp'] = mean_color_temp + 10
        else:
            service_data['color_temp'] = 250
        self.call_service(service_call, **service_data)

    def state_change(self, sensor, attribute, old, new, kwargs):
        mean_brightness, mean_color_temp = self.mean_vals()
        service_data = self.service_data.copy()
        service_call = "light/turn_on"
        now = datetime.datetime.now()
        interval = 1
        target = now + timedelta(seconds=interval)
        if new == 'toggle':
            service_call = "light/toggle"
        elif new == 'brightness_up_click' and mean_brightness < 245:
            service_data['brightness_step'] = 10
        elif new == 'brightness_down_click' and mean_brightness > 10:
            service_data['brightness_step'] = -10
        elif new == 'brightness_up_click' and mean_brightness >= 245:
            service_data['brightness'] = 10
        elif new == 'brightness_down_click' and mean_brightness <= 10:
            service_data['brightness'] = 255
        elif new == 'arrow_right_click' and mean_color_temp > 250:
            service_data['color_temp'] = mean_color_temp - 10
        elif new == 'arrow_left_click' and mean_color_temp < 500 and mean_color_temp !=0:
            service_data['color_temp'] = mean_color_temp + 10
        elif new == 'arrow_right_click' and mean_color_temp <= 250 and mean_color_temp !=0:
            service_data['color_temp'] = 500
        elif new == 'arrow_left_click' and mean_color_temp >= 500:
            service_data['color_temp'] = 250
        elif new == 'brightness_up_hold':
            self.bu_handler = self.run_every(self.brightness_up_hold,target,interval)
            return
        elif new == 'brightness_up_release':
            if self.bu_handler is not None:
                self.cancel_timer(self.bu_handler)
                self.bu_handler = None
        elif new == 'brightness_down_hold':
            self.bd_handler = self.run_every(self.brightness_down_hold,target,interval)
            return
        elif new == 'brightness_down_release':
            if self.bd_handler is not None:
                self.cancel_timer(self.bd_handler)
                self.bd_handler = None
        elif new == 'arrow_right_hold':
            self.ar_handler = self.run_every(self.arrow_right_hold,target,interval)
            return
        elif new == 'arrow_right_release':
            if self.ar_handler is not None:
                self.cancel_timer(self.ar_handler)
                self.ar_handler = None
        elif new == 'arrow_left_hold':
            self.al_handler = self.run_every(self.arrow_left_hold,target,interval)
            return
        elif new == 'arrow_left_release':
            if self.al_handler is not None:
                self.cancel_timer(self.al_handler)
                self.al_handler = None
        elif new == 'rotate_stop':
            brightness = self.get_state(sensor, attribute="brightness")
            if brightness is not None:
                self.turn_on(entity_id = light, brightness = brightness)
        if new != '':
            self.log(service_data)
            self.call_service(service_call, **service_data)
