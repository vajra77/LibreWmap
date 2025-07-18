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
            display: inline-block;
        """

        if self.alarm == 'ok':
            css += """
                animation: blink 3s linear infinite; 
                /* background: radial-gradient(rgb(68,206,27,1.0), rgb(255,255,255,0.2)); */
            }
            """
        elif self.alarm == 'warn':
            css += """
                animation: blink 1.5s linear infinite; 
                /* background: radial-gradient(rgb(242,161,52,1.0), rgb(255,255,255,0.2)); */
            }
            """
        else:
            css += """
                animation: blink 0.5s linear infinite; 
                /* background: radial-gradient(rgb(229,31,31,1.0), rgb(255,255,255,0.2)); */
            }
            """

        css += f""""
        .{self.name}:hover {{
            animation: none;
        }}
        
        .{self.name} p {{
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            background-color: #efefef;
        }}
        """

        css += f""" 
        .{self.name} img.svg-filter {{
            padding: 2px;
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
            return f"<p><img class='svg-filter' src='images/temp_up.svg'>{self.last}ºC</p>\n"
        elif self.trend < 0:
            return f"<p><img class='svg-filter' src='images/temp_down.svg'>{self.last}ºC</p>\n"
        else:
            return f"<p><img class='svg-filter' src='images/temp.svg'>{self.last}ºC</p>\n"


    def update(self, api_url, api_key):
        url = f"{api_url}/devices/{self.device_id}/health/temperature/{self.id}"
        response = requests.get(url=url, headers={"X-Auth-Token": api_key})
        data = response.json()

        t_prev = data['graphs'][0]['sensor_prev']
        t_cur = data['graphs'][0]['sensor_current']
        t_warn = data['graphs'][0]['sensor_limit_warn']
        t_crit = data['graphs'][0]['sensor_limit']

        if t_warn is None:
            t_warn = 30.0

        if t_crit is None:
            t_crit = 35.0

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