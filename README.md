<!--
title: "BME280 sensor monitoring with netdata"
custom_edit_url: https://github.com/netdata/netdata/edit/master/collectors/python.d.plugin/bme280/README.md
sidebar_label: "BME280"
-->

# BME280 sensor monitoring with netdata

Displays a graph of the temperature, humidity, and pressure from a BME280 sensor.

## Requirements
 - Adafruit Circuit Python BME280 library
 - Adafruit BME280 I2C Sensor (Product ID: 2652)
 - Python 3 (Adafruit libraries are not Python 2.x compatible)


It produces the following charts:
1. **Temperature**
2. **Humidity**
3. **Pressure**

## Configuration

Allow the `netdata` user to access the I2C interface.

```bash
sudo usermod -a -G i2c netdata
```

Edit the `python.d/bme280.conf` configuration file using `edit-config` from the Netdata [config
directory](/docs/configure/nodes.md), which is typically at `/etc/netdata`.

```bash
cd /etc/netdata     # Replace this path with your Netdata config directory, if different
sudo ./edit-config python.d/bme280.conf
```

Raspberry Pi Instructions:

Hardware install:
Connect the BME280 to the Raspberry Pi I2C pins

Raspberry Pi 3B/4 Pins:

- Board 3.3V (pin 1) to sensor VIN (pin 1)
- Board SDA (pin 3) to sensor SDA (pin 2)
- Board GND (pin 6) to sensor GND (pin 3)
- Board SCL (pin 5) to sensor SCL (pin 4)

You may also need to add two I2C pullup resistors if your board does not already have them. The Raspberry Pi
does have internal pullup resistors but it doesn't hurt to add them anyway. You can use 2.2K - 10K but we will
just use 10K. The resistors go from VDD to SCL and SDA each.

Software install:
- `sudo pip3 install adafruit-circuitpython-bme280`
- `sudo usermod -a -G i2c netdata`
- edit `/etc/netdata/netdata.conf`
- find `[plugin:python.d]`
- add  `command options = -ppython3`
- save the file.
- restart the netdata service.
- check the dashboard.
