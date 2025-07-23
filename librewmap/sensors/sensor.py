from dataclasses import dataclass, field


@dataclass
class Sensor:
    id: int
    device_id: int
    name: str
    label: str
    top: int
    left: int
    trend: int
    last: int or float
    alarm: str

    @property
    def type(self):
        return "generic"

    @property
    def fmt_label(self) -> str:
        return self.label

    @property
    def html(self) -> str:
        return ""

    @property
    def width(self) -> int:
        match self.alarm:
            case 'ok':
                return 30
            case 'warn':
                return 40
            case 'crit':
                return 60
            case _:
                return 20

    @property
    def blink(self) -> float:
        match self.alarm:
            case "ok":
                return 3
            case "warn":
                return 1.5
            case "crit":
                return 0.5
            case _:
                return 0.5

    @property
    def color_filter(self) -> str:
        return ""

    @property
    def image(self) -> str:
        return "images/ok.svg"

    def update(self, api_url, api_key):
        raise NotImplementedError()

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data["id"],
            device_id=data["device_id"],
            name=data["name"],
            label=data["label"],
            top=data["top"],
            left=data["left"],
            trend=0,
            last=0,
            alarm='none',
        )
