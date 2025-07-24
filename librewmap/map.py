import yaml
from librewmap.sensors import Sensor, TemperatureSensor, HumiditySensor, StateSensor, InvertedStateSensor, \
                               LoadSensor, PowerSensor


class Map:

    def __init__(self, name, title, image, css, api_url, api_key, nms_url):
        self._name = name
        self._title = title
        self._image = image
        self._css = css
        self._api_url = api_url
        self._api_key = api_key
        self._nms_url = nms_url
        self._sensors = []

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title

    @property
    def image(self):
        return self._image

    @property
    def css(self):
        return self._css

    @property
    def api_url(self):
        return self._api_url

    @property
    def api_key(self):
        return self._api_key

    @property
    def nms_url(self):
        return self._nms_url

    @property
    def sensors(self):
        return self._sensors

    def register_sensor(self, sensor: Sensor):
        self._sensors.append(sensor)

    def retrieve_data(self):
        for sensor in self._sensors:
            try:
                sensor.update(self._api_url, self._api_key)
            except Exception as e:
                print(f"[ERR]: sensor {sensor.name} = {e}")
                continue

    @property
    def alarm(self):
        result = False
        for sensor in self._sensors:
            if sensor.alarm != "ok":
                result = True
                break
        return result

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            conf = yaml.safe_load(f)

        this_map = cls(
            name=conf['map']['name'],
            title=conf['map']['title'],
            image=conf['map']['image'],
            css=conf['map']['css'],
            api_url=conf['map']['api_url'],
            api_key=conf['map']['api_key'],
            nms_url=conf['map']['nms_url'],
        )

        for sconf in conf['sensors']:
            match sconf['type']:
                case 'temperature':
                    sensor = TemperatureSensor.from_json(sconf)
                case 'humidity':
                    sensor = HumiditySensor.from_json(sconf)
                case 'state':
                    sensor = StateSensor.from_json(sconf)
                case 'inverted_state':
                    sensor = InvertedStateSensor.from_json(sconf)
                case 'load':
                    sensor = LoadSensor.from_json(sconf)
                case 'power':
                    sensor = PowerSensor.from_json(sconf)
                case _:
                    raise ValueError('Unknown sensor type')
            this_map.register_sensor(sensor)

        return this_map

