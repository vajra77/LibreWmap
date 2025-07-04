from .sensor import Sensor


class BinarySensor(Sensor):

    @property
    def type(self) -> str:
        return "binary"
