from .sensor import Sensor
import requests


class StateSensor(Sensor):

    @property
    def type(self) -> str:
        return "state"

    @property
    def html(self) -> str:
        result = f"<p><i class='fa-solid fa-bell'></i>&nbsp;{self.name}</p>\n"
        return result

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
            background: radial-gradient(rgb(193,202,255,1.0), rgb(255,255,255,0.2));
            """
        elif self.alarm == 'warn':
            css += """
            height: 100px;
            width: 100px;
            animation: blink 1.5s linear infinite; 
            background: radial-gradient(rgb(226,193,255,1.0), rgb(255,255,255,0.2));
            """
        else:
            css += """
            height: 120px;
            width: 120px;
            animation: blink 0.5s linear infinite; 
            background: radial-gradient(rgb(244,71,252,1.0), rgb(255,255,255,0.2));
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
