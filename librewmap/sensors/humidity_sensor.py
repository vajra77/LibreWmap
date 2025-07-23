import requests
from .sensor import Sensor


class HumiditySensor(Sensor):

    @property
    def type(self) -> str:
        return "humidity"

    @property
    def color_filter(self):
        match self.alarm:
            case "ok":
                return "invert(84%) sepia(51%) saturate(289%) hue-rotate(162deg) brightness(99%) contrast(94%)"
            case "warn":
                return "invert(49%) sepia(25%) saturate(1226%) hue-rotate(160deg) brightness(87%) contrast(96%"
            case "crit":
                return "invert(44%) sepia(70%) saturate(6957%) hue-rotate(205deg) brightness(92%) contrast(104%)"

    @property
    def image(self) -> str:
        return "images/drop.svg"

    @property
    def fmt_label(self) -> str:
        return f"{self.last}&percnt;"

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
