

class Sensor:

    def __init__(self, id, device_id, name, label, top, left, trend, last, alarm):
        self._id = id
        self._device_id = device_id
        self._name = name
        self._label = label
        self._top = top
        self._left = left
        self._trend = trend
        self._last = last
        self._alarm = alarm

    @property
    def id(self) -> str:
        return self._id

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def label(self) -> str:
        return self._label

    @property
    def top(self) -> str:
        return self._top

    @property
    def left(self) -> str:
        return self._left

    @property
    def trend(self) -> str:
        return self._trend

    @property
    def last(self) -> str:
        return self._last

    @property
    def alarm(self) -> str:
        return self._alarm

    @property
    def type(self):
        return "generic"

    @property
    def html(self) -> str:
        return ""

    @property
    def width(self) -> int:
        match self._alarm:
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
        match self._alarm:
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
