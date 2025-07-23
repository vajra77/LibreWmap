import requests
from .sensor import Sensor


class LoadSensor(Sensor):

    @property
    def type(self) -> str:
        return "load"

    @property
    def color_filter(self):
        match self.alarm:
            case "ok":
                return "invert(60%) sepia(51%) saturate(5443%) hue-rotate(86deg) brightness(121%) contrast(125%)"
            case "warn":
                return "invert(65%) sepia(82%) saturate(519%) hue-rotate(0deg) brightness(103%) contrast(104%)"
            case "crit":
                return "invert(18%) sepia(97%) saturate(6531%) hue-rotate(358deg) brightness(103%) contrast(112%)"

    @property
    def image(self) -> str:
        return "images/pwbank.svg"

    @property
    def label(self) -> str:
        return f"{self.label} ({self.last}&percnt;)"

    def update(self, api_url, api_key):
        url = f"{api_url}/devices/{self.device_id}/health/load/{self.id}"
        response = requests.get(url=url, headers={"X-Auth-Token": api_key})
        data = response.json()

        t_prev = data['graphs'][0]['sensor_prev']
        t_cur = data['graphs'][0]['sensor_current']
        t_warn = data['graphs'][0]['sensor_limit_warn']
        t_crit = data['graphs'][0]['sensor_limit']

        if t_warn is None:
            t_warn = 75.0

        if t_crit is None:
            t_crit = 90.0

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