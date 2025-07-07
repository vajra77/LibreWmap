import requests
from .sensor import Sensor


class TemperatureSensor(Sensor):

    @property
    def type(self) -> str:
        return "temperature"


    @property
    def css(self) -> str:
        css = f"""
        .{self.name} {{
            position: absolute;
            top: {self.top}px;
            left: {self.left}px;
        """

        if self.alarm == 'ok':
            css += """
                height: 80px;
                width: 80px;
                animation: blink 3s linear infinite; 
                background: radial-gradient(rgb(68,206,27,1.0), rgb(255,255,255,0.2));
            """
        elif self.alarm == 'warn':
            css += """
                height: 100px;
                width: 100px;
                animation: blink 1.5s linear infinite; 
                background: radial-gradient(rgb(242,161,52,1.0), rgb(255,255,255,0.2));
            """
        else:
            css += """
                height: 120px;
                width: 120px;
                animation: blink 0.5s linear infinite; 
                background: radial-gradient(rgb(229,31,31,1.0), rgb(255,255,255,0.2));
            """

        css += f"""
            border-radius: 50%;
            display: inline-block;
        }} 
        
        .{self.name}:hover {{
            animation: none;
        }}

        .{self.name} p {{
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            color: white;
        """

        if self.alarm == 'ok':
            css += """
                    height: 40px;
            """
        elif self.alarm == 'warn':
            css += """
                height: 60px
            """
        else:
            css += """
                height: 80px
            """

        return css


    @property
    def html(self) -> str:

        if self.trend > 0:
            result = f"<p><i class='fa-solid fa-temperature-arrow-up'></i><i class='fa-solid fa-arrow-up'></i>&nbsp;{self.last}</p>\n"
        elif self.trend < 0:
            result = f"<p><i class='fa-solid fa-temperature-arrow-down'></i><i class='fa-solid fa-arrow-down'></i>&nbsp;{self.last}</p>\n"
        else:
            result = f"<p><i class='fa-solid fa-temperature-half'></i>&nbsp;&nbsp;{self.last}</p>\n"

        return result


    def update(self, api_url, api_key):
        url = f"{api_url}/devices/{self.device_id}/health/temperature/{self.id}"
        response = requests.get(url=url, headers={"X-Auth-Token": api_key})
        data = response.json()

        t_prev = data['graphs'][0]['sensor_prev']
        t_cur = data['graphs'][0]['sensor_current']
        t_warn = data['graphs'][0]['sensor_limit_warn']
        t_crit = data['graphs'][0]['sensor_limit']

        if t_prev > t_cur:
            self.trend = -1
        elif t_prev < t_cur:
            self.trend = 1
        else:
            self.trend = 0

        if t_warn is not None:
            if t_cur < t_warn:
                self.alarm = 'ok'
            elif t_warn <= t_cur < t_crit:
                self.alarm = 'warn'
            else:
                self.alarm = 'crit'

        self.last = t_cur