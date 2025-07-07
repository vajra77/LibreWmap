import yaml
from dataclasses import dataclass
from typing import List
from librewmap.sensors import Sensor, TemperatureSensor, HumiditySensor, StateSensor


@dataclass
class Map:
    name: str
    title: str
    image: str
    css: str
    next: str
    api_url: str
    api_key: str
    nms_url: str
    sensors: List[Sensor]

    def register_sensor(self, sensor: Sensor):
        self.sensors.append(sensor)

    def retrieve_data(self):
        for sensor in self.sensors:
           sensor.update(self.api_url, self.api_key)

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            conf = yaml.safe_load(f)

        this_map = cls(
            name=conf['map']['name'],
            title=conf['map']['title'],
            image=conf['map']['image'],
            css=conf['map']['css'],
            next=conf['map']['next'],
            api_url=conf['map']['api_url'],
            api_key=conf['map']['api_key'],
            nms_url=conf['map']['nms_url'],
            sensors=[]
        )

        for sconf in conf['sensors']:
            match sconf['type']:
                case 'temperature':
                    sensor = TemperatureSensor.from_json(sconf)
                case 'humidity':
                    sensor = HumiditySensor.from_json(sconf)
                case 'state':
                    sensor = StateSensor.from_json(sconf)
                case _:
                    raise ValueError('Unknown sensor type')
            this_map.register_sensor(sensor)

        return this_map



