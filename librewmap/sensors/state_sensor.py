from .sensor import Sensor
import requests


class StateSensor(Sensor):

    @property
    def type(self) -> str:
        return "state"

    @property
    def html(self) -> str:
        match self.alarm:
            case "ok":
                return f"<p><img class='svg-filter' src='images/check.svg'>{self.name}</p>\n"
            case "warn":
                return f"<p><img class='svg-filter' src='images/bell.svg'>{self.name}</p>\n"
            case "crit":
                return f"<p><img class='svg-filter' src='images/bell.svg'>{self.name}</p>\n"
        return ""

    @property
    def css(self) -> str:

        css = f"""
        .{self.name} {{
            position: absolute;
            top: {self.top}px;
            left: {self.left}px;
        """

        match self.alarm:
            case "ok":
                css += """
                    animation: blink 3s linear infinite;
                }
                """
            case 'warn':
                css += """
                    animation: blink 1.5s linear infinite; 
                }
                """
            case 'crit':
                css += """
                    animation: blink 0.5s linear infinite; 
                }
                """

        css += f"""
        .{self.name}:hover {{
            animation: none;
        }}

        .{self.name} p {{
            padding: 3px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
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

    def update(self, api_url, api_key):
        url = f"{api_url}/devices/{self.device_id}/health/state/{self.id}"
        response = requests.get(url=url, headers={"X-Auth-Token": api_key})
        data = response.json()

        t_cur = data['graphs'][0]['sensor_current']

        if t_cur is not None:
            if t_cur == 1:
                self.alarm = 'crit'
            else:
                self.alarm = 'ok'
        else:
            self.alarm = 'warn'

        self.last = t_cur
