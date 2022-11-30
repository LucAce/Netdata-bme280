# _*_ coding: utf-8 _*_
# Description: BME280 netdata module
# Author: LucAce
# SPDX-License-Identifier: GPL-3.0-or-Later

try:
    import board
    import busio
    from adafruit_bme280 import basic as adafruit_bme280

    HAS_BME280 = True
except ImportError:
    HAS_BME280 = False

from bases.FrameworkServices.SimpleService import SimpleService

# Default module values (can be overridden per job in `config`)
update_every = 5

# Default precision value
precision_scaling = 100

ORDER = [
    'temperature',
    'humidity',
    'pressure',
    'altitude'
]

CHARTS = {
    'temperature': {
        'options': [None, 'Temperature', 'celsius', 'temperature', 'bme280.temperature', 'line'],
        'lines': [
            ['temperature', 'temperature', 'absolute', 1, precision_scaling]
        ]
    },
    'humidity': {
        'options': [None, 'Relative Humidity', 'percent', 'humidity', 'bme280.humidity', 'line'],
        'lines': [
            ['humidity', 'humidity', 'absolute', 1, precision_scaling]
        ]
    },
    'pressure': {
        'options': [None, 'Barometric Pressure', 'hPa', 'pressure', 'bme280.pressure', 'line'],
        'lines': [
            ['pressure', 'pressure', 'absolute', 1, precision_scaling]
        ]
    },
    'altitude': {
        'options': [None, 'Altitude', 'meters', 'altitude', 'bme280.altitude', 'line'],
        'lines': [
            ['altitude', 'altitude', 'absolute', 1, precision_scaling]
        ]
    }
}


class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.i2c_address = int(self.configuration.get('i2c_address', '0x77'))
        self.sea_level_pressure = float(self.configuration.get('sea_level_pressure', '1013.25'))
        self.bme = None

    def check(self):
        if not HAS_BME280:
            self.error("Could not find the Adafruit_CircuitPython_BME280 package.")
            return False

        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.bme = adafruit_bme280.Adafruit_BME280_I2C(i2c, self.i2c_address)
            self.bme.sea_level_pressure = self.sea_level_pressure

        except ValueError as error:
            self.error("Error on creating I2C shared bus: {0}".format(error))
            return False

        return True

    def get_data(self):
        try:
            return {
                'temperature': int(self.bme.temperature * precision_scaling),
                'humidity': int(self.bme.relative_humidity * precision_scaling),
                'pressure': int(self.bme.pressure * precision_scaling),
                'altitude': int(self.bme.altitude * precision_scaling)
            }

        except (OSError, RuntimeError) as error:
            self.error(error)
            return None
