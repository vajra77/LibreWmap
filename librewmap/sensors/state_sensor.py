from .sensor import Sensor
import requests


class StateSensor(Sensor):

    @property
    def type(self) -> str:
        return "state"

    @property
    def image(self) -> str:
        match self._alarm:
            case "ok":
                return "images/check.svg"
            case "warn":
                return "images/bell.svg"
            case "crit":
                return "images/bell.svg"
            case _:
                return ""

    @property
    def color_filter(self) -> str:
        match self._alarm:
            case "ok":
                return "invert(60%) sepia(51%) saturate(5443%) hue-rotate(86deg) brightness(121%) contrast(125%)"
            case "warn":
                return "invert(65%) sepia(82%) saturate(519%) hue-rotate(0deg) brightness(103%) contrast(104%)"
            case "crit":
                return "invert(18%) sepia(97%) saturate(6531%) hue-rotate(358deg) brightness(103%) contrast(112%)"
            case _:
                return ""

    def update(self, api_url, api_key):
        url = f"{api_url}/devices/{self.device_id}/health/state/{self.id}"
        response = requests.get(url=url, headers={"X-Auth-Token": api_key})
        data = response.json()

        t_cur = data['graphs'][0]['sensor_current']

        if t_cur is not None:
            if t_cur == 1:
                self._alarm = 'crit'
            else:
                self._alarm = 'ok'
        else:
            self._alarm = 'warn'

        self._last = t_cur
