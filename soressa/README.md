# Soressa

The "Bus Tracking Device"

This module runs on ESP8266 and send messagens to a MQTT Broker.

## Requirements

- ESP8266 (ESP-12 or ESP-7)
- NodeMCU Firmware
- GPS Module (u-blox NEO-6m)
- RTC Module (DS3231)

## NodeMCU required modules

- bit
- file
- GPIO
- i2c
- MQTT (with SSL)
- node
- timer
- UART
- WiFi

You must use branch `dev096` to get everythong working.

Custom builds can be made at [NodeMCU custom builds](http://frightanic.com/nodemcu-custom-build/)

## Pinout

TODO

## Setup

To get Soressa working, connect to Wifi and MQTT, you need to add configuration files.

### For WIFI

You need to save `wpa.conf` to ESP file system.
This is a plain text file with SSID, password and BSSID.
The file can have multiple lines.

For example:

```
MyWIFI,MyPWD,00:0a:95:9d:68:15
OtherWIFI,OtherPWD,00:0a:95:9d:68:16
```

### For MQTT

TODO

## Location

Soressa only knows how to work with NMEA 0183 protocol and only accepet messagens from GPS, not GLONASS.

The GPS module is activated in intervals. Wake up for 10 sec and sleep for 30 sec.
This avoid massive data over MQTT, which makes MQTT breaks easily.

## LEDs

| Color  | Meaning   | Pin | GPIO    |
|:------:|:---------:|:---:|:-------:|
| Red    | ERROR LED | 2   | GPIO 4  |
| Blue   | GPS LED   | 5   | GPIO 14 |
| Yellow | MQTT LED  | 0   | GPIO 16 |
| Green  | WIFI LED  | 1   | GPIO 5  |

All LEDs have a meaning:

- All ON, boot time
- Green blinkng is WIFI connecting
- Green ON is WIFI connected
- Red ON is error (WIFI, MQTT...)
- Yellow ON is MQTT connected
- Blue ON is GPS ON

## Problems

The most annoying problem is that ESP or NodeMCU crashes a lot. It's really annoying, seriously.

- The DNS crashes
- ESP get out of memory (I've made a lot of changes to solve this)
- MQTT goes offline with no reason
- NodeMCU get in "Panic"
- UART event unbind sometimes and the GPS start to send NMEA messages to NodeMCU
- Sometimes ESP get unresponsive, like frozen.

## License

MIT
