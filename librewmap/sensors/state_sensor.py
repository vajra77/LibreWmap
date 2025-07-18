from .sensor import Sensor
import requests


class StateSensor(Sensor):

    @property
    def type(self) -> str:
        return "state"

    @property
    def html(self) -> str:
        if self.alarm == 'warn' or self.alarm == 'crit':
            result = f"<p><img class='svg-filter' src='images/bell_alarm.svg'> {self.name}</p>\n"
        else:
            result = f"<p><img class='svg-filter' src='images/ok.svg'> {self.name}</p>\n"

        return result

    @property
    def css(self) -> str:

        if self.alarm == 'ok':
            css = """
            .svg-filter {
                fill: green;
                width: 20px;
            }
            """
        elif self.alarm == 'warn':
            css = """
                .svg-filter {
                    fill: orange;
                    width: 30px;
                }
                """
        elif self.alarm == 'crit':
            css = """
                .svg-filter {
                    fill: red;
                    width: 40px;
                }
                """
        else:
            css = ""

        css += f"""
        .{self.name} {{
            position: absolute;
            top: {self.top}px;
            left: {self.left}px;
        """

        if self.alarm == 'ok':
            css += """
            width: 80px;
            height: 80px;
            animation: blink 3s linear infinite;
            /* background: radial-gradient(rgb(52,73,94,1.0), rgb(255,255,255,0.2)); */
            """
        elif self.alarm == 'warn':
            css += """
            height: 100px;
            width: 100px;
            animation: blink 1.5s linear infinite; 
            /* background: radial-gradient(rgb(211,84,0,1.0), rgb(255,255,255,0.2)); */
            """
        else:
            css += """
            height: 100px;
            width: 100px;
            animation: blink 0.5s linear infinite; 
            /* background: radial-gradient(rgb(176,58,46,1.0), rgb(255,255,255,0.2)); */
            """

        css += f"""
        }}
        
        .{self.name}:hover {{
            animation: none;
        }}

        .{self.name} p {{
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
        """

        if self.alarm == 'ok':
            css += """
            height: 40px;
            color: green;
            """
        elif self.alarm == 'warn':
            css += """
            height: 60px
            color: orange;
            """
        else:
            css += """
            height: 80px
            color: red;
            """

        css += "}"

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
