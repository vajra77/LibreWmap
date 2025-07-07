from .sensor import Sensor


class StateSensor(Sensor):

    @property
    def type(self) -> str:
        return "state"
