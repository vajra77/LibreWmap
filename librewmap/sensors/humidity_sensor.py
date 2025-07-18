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

        css += f""" 
        .{self.name} img.svg-filter {{
            padding-right: 10px;
        """

        match self.alarm:
            case "ok":
                css += """
                    width: 20px;
                    filter: invert(60%) sepia(51%) saturate(5443%) hue-rotate(86deg) brightness(121%) contrast(125%);
                }
                """
            case "warn":
                css += """
                    width: 30px;
                    filter: invert(65%) sepia(82%) saturate(519%) hue-rotate(0deg) brightness(103%) contrast(104%);
                }
                """
            case "crit":
                css += """
                    width: 40px;
                    filter: invert(18%) sepia(97%) saturate(6531%) hue-rotate(358deg) brightness(103%) contrast(112%);
                }
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
