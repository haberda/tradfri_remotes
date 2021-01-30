import hassapi as hass
import datetime
from datetime import timedelta

class tradfri_remotes(hass.Hass):
    def initialize(self):
        self.sensors = self.args.get('sensors', None)
        self.lights = self.args.get('lights', None)
        self.device_ieee = self.args.get('device_ieee', None)
        self.brightness_step = self.args.get('brightness_step', 25)
        self.prefer_rgb = self.args.get('prefer_rgb', True)
        self.max_kelvin = self.args.get('max_kelvin', 5000)
        self.min_kelvin = self.args.get('min_kelvin', 2200)
        self.color_step = 200
        self.kelvin_table = {
            1000: [255, 56, 0],
            1100: [255, 71, 0],
            1200: [255, 83, 0],
            1300: [255, 93, 0],
            1400: [255, 101, 0],
            1500: [255, 109, 0],
            1600: [255, 115, 0],
            1700: [255, 121, 0],
            1800: [255, 126, 0],
            1900: [255, 131, 0],
            2000: [255, 138, 18],
            2100: [255, 142, 33],
            2200: [255, 147, 44],
            2300: [255, 152, 54],
            2400: [255, 157, 63],
            2500: [255, 161, 72],
            2600: [255, 165, 79],
            2700: [255, 169, 87],
            2800: [255, 173, 94],
            2900: [255, 177, 101],
            3000: [255, 180, 107],
            3100: [255, 184, 114],
            3200: [255, 187, 120],
            3300: [255, 190, 126],
            3400: [255, 193, 132],
            3500: [255, 196, 137],
            3600: [255, 199, 143],
            3700: [255, 201, 148],
            3800: [255, 204, 153],
            3900: [255, 206, 159],
            4000: [255, 209, 163],
            4100: [255, 211, 168],
            4200: [255, 213, 173],
            4300: [255, 215, 177],
            4400: [255, 217, 182],
            4500: [255, 219, 186],
            4600: [255, 221, 190],
            4700: [255, 223, 194],
            4800: [255, 225, 198],
            4900: [255, 227, 202],
            5000: [255, 228, 206],
            5100: [255, 230, 210],
            5200: [255, 232, 213],
            5300: [255, 233, 217],
            5400: [255, 235, 220],
            5500: [255, 236, 224],
            5600: [255, 238, 227],
            5700: [255, 239, 230],
            5800: [255, 240, 233],
            5900: [255, 242, 236],
            6000: [255, 243, 239],
            6100: [255, 244, 242],
            6200: [255, 245, 245],
            6300: [255, 246, 247],
            6400: [255, 248, 251],
            6500: [255, 249, 253],
            6600: [254, 249, 255],
            6700: [252, 247, 255],
            6800: [249, 246, 255],
            6900: [247, 245, 255],
            7000: [245, 243, 255],
            7100: [243, 242, 255],
            7200: [240, 241, 255],
            7300: [239, 240, 255],
            7400: [237, 239, 255],
            7500: [235, 238, 255],
            7600: [233, 237, 255],
            7700: [231, 236, 255],
            7800: [230, 235, 255],
            7900: [228, 234, 255],
            8000: [227, 233, 255],
            8100: [225, 232, 255],
            8200: [224, 231, 255],
            8300: [222, 230, 255],
            8400: [221, 230, 255],
            8500: [220, 229, 255],
            8600: [218, 229, 255],
            8700: [217, 227, 255],
            8800: [216, 227, 255],
            8900: [215, 226, 255],
            9000: [214, 225, 255],
            9100: [212, 225, 255],
            9200: [211, 224, 255],
            9300: [210, 223, 255],
            9400: [209, 223, 255],
            9500: [208, 222, 255],
            9600: [207, 221, 255],
            9700: [207, 221, 255],
            9800: [206, 220, 255],
            9900: [205, 220, 255],
            10000: [207, 218, 255],
            10100: [207, 218, 255],
            10200: [206, 217, 255],
            10300: [205, 217, 255],
            10400: [204, 216, 255],
            10500: [204, 216, 255],
            10600: [203, 215, 255],
            10700: [202, 215, 255],
            10800: [202, 214, 255],
            10900: [201, 214, 255],
            11000: [200, 213, 255],
            11100: [200, 213, 255],
            11200: [199, 212, 255],
            11300: [198, 212, 255],
            11400: [198, 212, 255],
            11500: [197, 211, 255],
            11600: [197, 211, 255],
            11700: [197, 210, 255],
            11800: [196, 210, 255],
            11900: [195, 210, 255],
            12000: [195, 209, 255]}
        self.kelvin_list = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900,
                    2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900,
                    3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900,
                    4000, 4100, 4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900,
                    5000, 5100, 5200, 5300, 5400, 5500, 5600, 5700, 5800, 5900,
                    6000, 6100, 6200, 6300, 6400, 6500, 6600, 6700, 6800, 6900,
                    7000, 7100, 7200, 7300, 7400, 7500, 7600, 7700, 7800, 7900,
                    8000, 8100, 8200, 8300, 8400, 8500, 8600, 8700, 8800, 8900,
                    9000, 9100, 9200, 9300, 9400, 9500, 9600, 9700, 9800, 9900,
                    10000, 10100, 10200, 10300, 10400, 10500, 10600, 10700, 10800, 10900,
                    11000, 11100, 11200, 11300, 11400, 11500, 11600, 11700, 11800, 11900,
                    12000]
        self.bu_handler = None
        self.bd_handler = None
        self.al_handler = None
        self.ar_handler = None
        if self.lights is not None and (self.sensors is not None or self.device_ieee is not None):
            if isinstance(self.lights, str):
                self.lights = self.lights.split(',')
            if self.sensors is not None:
                if isinstance(self.sensors, str):
                    self.sensors = self.sensors.split(',')
                for sensor in self.sensors:
                    self.listen_state(self.state_change, sensor)
            if self.device_ieee is not None:
                if isinstance(self.device_ieee, str):
                    self.device_ieee = self.device_ieee.split(',')
                if self.device_ieee is not None:
                    self.listen_event(self.event_change,'zha_event')
        else:
            self.log('Either no lights or no remotes defined. Exiting.')

    def min_rgb (self, RGB=[255,255,255]):
        # Find the best match between current rgb color and color temperature
        min_list = []
        for i in range(0, len(self.kelvin_list)):
            tmp = [x1-x2 for x1,x2 in zip(RGB,self.kelvin_table[self.kelvin_list[i]])]
            res =  [abs(ele) for ele in tmp] 
            min_list.append(res)
        minrgb=min_list.index(min(min_list))
        return minrgb

    def brightness_up (self, kwargs):
        for light in self.lights:
            service_call = "light/turn_on"
            self.call_service(service_call, entity_id = light, brightness_step = self.brightness_step)

    def brightness_down (self, kwargs):
        for light in self.lights:
            if self.get_state(light) == 'on':
                service_call = "light/turn_on"
                self.call_service(service_call, entity_id = light, brightness_step = (self.brightness_step*-1))

    def arrow_right (self, kwargs):
        for light in self.lights:
            if self.get_state(light) == 'on':
                service_call = "light/turn_on"
                rgb_color = self.get_state(light, attribute="rgb_color")
                ct = self.get_state(light, attribute="color_temp")
                if ct is not None and not (self.prefer_rgb and rgb_color is not None):
                    self.log(light+' ct')
                    ctk = int(1000000/ct)
                    next_temp = ctk + self.color_step
                    if next_temp >= self.max_kelvin:
                        self.call_service(service_call, entity_id = light, kelvin = self.min_kelvin)
                    else:
                        self.call_service(service_call, entity_id = light, kelvin = next_temp)
                elif rgb_color is not None:
                    self.log(light+' rgb')
                    minrgb = self.min_rgb(rgb_color)
                    nextcolortmp = int(self.kelvin_list[minrgb]) + self.color_step
                    if nextcolortmp < self.max_kelvin:
                        nextrgb = self.kelvin_table[nextcolortmp]
                    else:
                        nextrgb = self.kelvin_table[self.min_kelvin]
                    self.call_service(service_call, entity_id = light, rgb_color = nextrgb)

    def arrow_left (self, kwargs):
        for light in self.lights:
            if self.get_state(light) == 'on':
                service_call = "light/turn_on"
                rgb_color = self.get_state(light, attribute="rgb_color")
                ct = self.get_state(light, attribute="color_temp")
                if ct is not None and (not self.prefer_rgb and rgb_color is not None):
                    ctk = int(1000000/ct)
                    next_temp = ctk - self.color_step
                    if next_temp <= self.min_kelvin:
                        self.call_service(service_call, entity_id = light, kelvin = self.max_kelvin)
                    else:
                        self.call_service(service_call, entity_id = light, kelvin = next_temp)
                elif rgb_color is not None:
                    minrgb = self.min_rgb(rgb_color)
                    nextcolortmp = int(self.kelvin_list[minrgb]) - self.color_step
                    if nextcolortmp > self.min_kelvin:
                        nextrgb = self.kelvin_table[nextcolortmp]
                    else:
                        nextrgb = self.kelvin_table[self.max_kelvin]
                    self.call_service(service_call, entity_id = light, rgb_color = nextrgb)

    def state_change (self, sensor, attribute, old, new, kwargs):
        self.run_in(self.adjust_light, 0, command=new, args=None)

    def event_change (self, event, data, kwargs):
        if not 'device_ieee' in data:
            return
        if not data['device_ieee'] in self.device_ieee:
            return
        self.run_in(self.adjust_light, 0, command=data['command'], args=data['args'])

    def adjust_light(self, kwargs):
        now = datetime.datetime.now()
        interval = 1
        target = now + timedelta(seconds=interval)
        if kwargs['command'] == 'toggle':
            service_call = "light/toggle"
            for light in self.lights:
                self.call_service(service_call, entity_id = light)
        elif (kwargs['command'] == 'press' and kwargs['args'] == [2,0,0]) or (kwargs['command'] == 'move_to_level_with_on_off' and kwargs['args'] == [254,0]):
            # Press and hold toggle button
            service_call = 'light/turn_on'
            min_list = []
            for i in range(0, len(self.kelvin_list)):
                min_list.append(abs(self.kelvin_list[i]-self.max_kelvin))
            min_num = min_list.index(min(min_list))
            for light in self.lights:
                self.call_service(service_call, entity_id = light)
                rgb_color = self.get_state(light, attribute="rgb_color")
                ct = self.get_state(light, attribute="color_temp")
                if ct is not None:
                    self.call_service(service_call, entity_id = light, brightness = 255, kelvin = self.max_kelvin)
                elif rgb_color is not None:
                    self.call_service(service_call, entity_id = light, brightness = 255, rgb_color = self.kelvin_table[self.kelvin_list[min_num]])
        elif kwargs['command'] == 'step_with_on_off' or kwargs['command'] == 'brightness_up_click': #Brightness up
            self.run_in(self.brightness_up, 0)
        elif kwargs['command'] == 'step' or kwargs['command'] == 'brightness_down_click': #Brightness down
            self.run_in(self.brightness_down, 0)
        elif (kwargs['command'] == 'press' and kwargs['args'] == [256,13,0]) or kwargs['command'] == 'arrow_right_click': #Arrow right
            self.run_in(self.arrow_right, 0)
        elif (kwargs['command'] == 'press' and kwargs['args'] == [257,13,0]) or kwargs['command'] == 'arrow_left_click': #Arrow left
            self.run_in(self.arrow_left, 0)
        elif (kwargs['command'] == 'move_with_on_off' and kwargs['args'] == [0,84]) or kwargs['command'] == 'brightness_up_hold': #Brightness up hold
            self.bu_handler = self.run_every(self.brightness_up,target,interval)
        elif (kwargs['command'] == 'move' and kwargs['args'] == [1,84]) or kwargs['command'] == 'brightness_down_hold': #Brightness down hold
            self.bd_handler = self.run_every(self.brightness_down,target,interval)
        elif (kwargs['command'] == 'hold' and kwargs['args'] == [3328,0]) or kwargs['command'] == 'arrow_right_hold': #Arrow right hold
            self.ar_handler = self.run_every(self.arrow_right,target,interval)
        elif (kwargs['command'] == 'hold' and kwargs['args'] == [3328,0]) or kwargs['command'] == 'arrow_left_hold': #Arrow left hold
            self.al_handler = self.run_every(self.arrow_left,target,interval)
        elif kwargs['command'] == 'stop' or kwargs['command'] == 'release' or kwargs['command'] == 'brightness_up_release' or kwargs['command'] == 'brightness_down_release':
            if self.bu_handler is not None:
                self.cancel_timer(self.bu_handler)
                self.bu_handler = None
            if self.bd_handler is not None:
                self.cancel_timer(self.bd_handler)
                self.bd_handler = None
            if self.ar_handler is not None:
                self.cancel_timer(self.ar_handler)
                self.ar_handler = None
            if self.al_handler is not None:
                self.cancel_timer(self.al_handler)
                self.al_handler = None
        elif (kwargs['command'] == 'move' or kwargs['command'] == 'move_with_on_off' or kwargs['command'] == 'move_to_level_with_on_off') and (kwargs['args'] == [0,195] or kwargs['args'] == [1,195] or kwargs['args'] == [255,1] or kwargs['args'] == [0,1] or kwargs['args'] == [0,70] or kwargs['args'] == [1,70]):
            service_call = 'light/turn_on'
            if kwargs['args'] == [0,195] or kwargs['args'] == [255,1] or kwargs['args'] == [0,70]:
                for light in self.lights:
                    self.call_service(service_call, entity_id = light, brightness_step = 25)
            elif kwargs['args'] == [1,195] or kwargs['args'] == [0,1] or kwargs['args'] == [1,70]:
                for light in self.lights:
                    self.call_service(service_call, entity_id = light, brightness_step = (25*-1))
        elif kwargs['command'] == 'rotate_stop':
            brightness = self.get_state(sensor, attribute="brightness")
            if brightness is not None:
                self.turn_on(entity_id = light, brightness = brightness)
