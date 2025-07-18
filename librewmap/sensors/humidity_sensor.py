import requests
from .sensor import Sensor


class HumiditySensor(Sensor):

    @property
    def type(self) -> str:
        return "humidity"

    @property
    def css(self) -> str:
        css = f"""
        .{self.name} {{
            position: absolute;
            top: {self.top}px;
            left: {self.left}px;
            display: inline-block;
        """

        match self.alarm:
            case "ok":
                css += """
                    animation: blink 3s linear infinite; 
                }
                """
            case "warn":
                css += """
                    animation: blink 1.5s linear infinite; 
                }
                """
            case "crit":
                css += """
                    animation: blink 0.5s linear infinite; 
                }
                """

        css += f"""
        .{self.name}:hover {{
            animation: none;
        }}

        .{self.name} p {{
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            color: white;
        }}
        """
        return css

    @property
    def html(self) -> str:

        if self.trend > 0:
            return f"<p><img src='images/drop.svg' class='svg-filter'>{self.last}<img src='images/up.svg'></p>"
        elif self.trend < 0:
            return f"<p><img src='images/drop.svg' class='svg-filter'>{self.last}<img src='images/down.svg'></p>"
        else:
            return f"<p><img src='images/drop.svg' class='svg-filter'>{self.last}</p>"


    def update(self, api_url, api_key):
        url = f"{api_url}/devices/{self.device_id}/health/humidity/{self.id}"
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
