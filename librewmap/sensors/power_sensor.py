import requests
from .sensor import Sensor


class PowerSensor(Sensor):

    @property
    def type(self) -> str:
        return "power"

    @property
    def color_filter(self):
        match self._alarm:
            case "ok":
                return "invert(60%) sepia(51%) saturate(5443%) hue-rotate(86deg) brightness(121%) contrast(125%)"
            case "warn":
                return "invert(65%) sepia(82%) saturate(519%) hue-rotate(0deg) brightness(103%) contrast(104%)"
            case "crit":
                return "invert(18%) sepia(97%) saturate(6531%) hue-rotate(358deg) brightness(103%) contrast(112%)"

    @property
    def image(self) -> str:
        return "images/power.svg"

    @property
    def label(self) -> str:
        value = self._last / 1000.0
        return f"{value:02}kW"

    def update(self, api_url, api_key):
        url = f"{api_url}/devices/{self.device_id}/health/load/{self.id}"
        response = requests.get(url=url, headers={"X-Auth-Token": api_key})
        data = response.json()

        t_prev = data['graphs'][0]['sensor_prev']
        t_cur = data['graphs'][0]['sensor_current']
        t_warn = data['graphs'][0]['sensor_limit_warn'] or 1000000
        t_crit = data['graphs'][0]['sensor_limit'] or 1000000

        if t_prev > t_cur:
            self._trend = -1
        elif t_prev < t_cur:
            self._trend = 1
        else:
            self._trend = 0

        if t_warn is not None:
            if t_cur < t_warn:
                self._alarm = 'ok'
            elif t_warn <= t_cur < t_crit:
                self._alarm = 'warn'
            else:
                self._alarm = 'crit'

        self._last = t_cur

