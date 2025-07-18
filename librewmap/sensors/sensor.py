from dataclasses import dataclass


@dataclass
class Sensor:
    id: int
    device_id: int
    name: str
    top: int
    left: int
    trend: int
    last: int or float
    alarm: str

    @property
    def type(self):
        return "generic"

    @property
    def html(self) -> str:
        return ""

    @property
    def width(self) -> int:
        return 20

    @property
    def css(self) -> str:
        return ""

    def update(self, api_url, api_key):
        raise NotImplementedError()

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data["id"],
            device_id=data["device_id"],
            name=data["name"],
            top=data["top"],
            left=data["left"],
            trend=0,
            last=0,
            alarm='none',
        )
