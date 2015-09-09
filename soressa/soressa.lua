MQTT_ADDRESS = "tcc.alexandrevicenzi.com"
MQTT_PORT = 1883
MQTT_AUTH_USER = "guest"
MQTT_AUTH_PWD = "guest"
MQTT_TIMEOUT = 120

WIFI_OK_LED = 1 -- pin 1 (GPIO 5)
WIFI_ERROR_LED = 2 -- pin 2 (GPIO 4)

WIFI_TMR = 0
MQTT_TMR = 1


function wifi_connecting()
    gpio.write(WIFI_OK_LED, gpio.LOW)
    gpio.write(WIFI_ERROR_LED, gpio.LOW)

    mqtt_client.close()

    wifi_state = false

    tmr.alarm(WIFI_TMR, 120, 1, function()
        if (wifi_state) then
            gpio.write(WIFI_OK_LED, gpio.HIGH)
        else
            gpio.write(WIFI_OK_LED, gpio.LOW)
        end
        wifi_state = not wifi_state
    end)
end

function wifi_connected()
    tmr.stop(WIFI_TMR)

    gpio.write(WIFI_OK_LED, gpio.HIGH)
    gpio.write(WIFI_ERROR_LED, gpio.LOW)

    mqtt_client:connect(MQTT_ADDRESS, MQTT_PORT, 0, function(cli)
        print("MQTT: Connected.")
    end)
end

function wifi_error()
    tmr.stop(WIFI_TMR)
    tmr.stop(MQTT_TMR)

    gpio.write(WIFI_OK_LED, gpio.LOW)
    gpio.write(WIFI_ERROR_LED, gpio.HIGH)

    mqtt_client.close()
end

function gpio_setup()
    gpio.mode(WIFI_OK_LED, gpio.OUTPUT)
    gpio.mode(WIFI_ERROR_LED, gpio.OUTPUT)
    gpio.write(WIFI_OK_LED, gpio.LOW)
    gpio.write(WIFI_ERROR_LED, gpio.LOW)
end

function wifi_setup()
    wifi.sta.eventMonReg(wifi.STA_IDLE, function()
        print("WIFI: Idle.")
        wifi.sta.connect()
    end)

    wifi.sta.eventMonReg(wifi.STA_WRONGPWD, function()
        wifi_error()
        print("WIFI: Wrong password!")
    end)

    wifi.sta.eventMonReg(wifi.STA_APNOTFOUND, function()
        wifi_error()
        print("WIFI: No AP found!")
    end)

    wifi.sta.eventMonReg(wifi.STA_FAIL, function()
        wifi_error()
        print("WIFI: Fail!")
    end)

    wifi.sta.eventMonReg(wifi.STA_GOTIP, function()
        wifi_connected()
        ip = wifi.sta.getip()
        print("WIFI: Connected. Got IP: " .. ip)
    end)

    wifi.sta.eventMonReg(wifi.STA_CONNECTING, function(prev_state)
        wifi_connecting()
        if (prev_state == wifi.STA_GOTIP) then
            print("WIFI: Connection Lost. Attempting to reconnect...")
        else
            print("WIFI: Connecting...")
        end
    end)

    wifi.setmode(wifi.STATION)
    wifi.sta.autoconnect(1)

    file.open("wifi.csv", "r")

    repeat
        line = file.readline()
        i, j = string.find(line, ";")
        ssid = string.sub(line, 0, i - 1)
        pwd = string.sub(line, i + 1, string.len(line))
        wifi.sta.config(ssid, pwd)
    until (line == nil)

    -- file.close()
end

function mqtt_setup()
    m = mqtt.Client("soressa", MQTT_TIMEOUT, MQTT_AUTH_USER, MQTT_AUTH_PWD)
    m:lwt("/lwt", "offline", 0, 0)

    m:on("connect", function(cli)
        print("WIFI: Connected to Broker.")

        cli:subscribe("/location", 0, function(cli)
            print("MQTT: Subscribed to channel.")
        end)

        tmr.alarm(MQTT_TMR, 2000, 1, function()
            mqtt_send()
        end)
    end)

    m:on("offline", function(cli)
        print("MQTT: Client Offline!")
        tmr.stop(MQTT_TMR)
    end)

    return m
end

function mqtt_send()
    lat = "-26.8956032" -- TODO
    lon = "-49.0794134" -- TODO
    ts = get_time_iso_8601()
    slug = "AAA1234" -- TODO
    msg = string.format("@%s,$s,%s,%s", lat, lon, ts, slug)
    mqtt_client:publish("/locator", msg, 0, 0, function(conn)
        print("MQTT: Message sent.")
    end)
end

-- I2C RTC is based on this link:
-- http://www.esp8266-projects.com/2015/03/pcf8563-real-time-clock-i2c-driver.html

function i2c_setup()
    i2c.setup(0, 6, 7, i2c.SLOW)
end

function to_decimal(val)
    local hl = bit.rshift(val, 4)
    local hh = bit.band(val, 0xf)
    local hr = string.format("%d%d", hl, hh)
    return string.format("%d%d", hl, hh)
end

function to_bcd(val)
    local d = string.format("%d", tonumber(val / 10))
    local d1 = tonumber(d * 10)
    local d2 = val - d1
    return tonumber(d * 16 + d2)
end

function get_time()
    i2c.start(0)
    i2c.address(0, 0x68, i2c.TRANSMITTER)
    i2c.write(0, 0x00) -- set DS3231 register pointer to 00h
    i2c.stop(0)

    i2c.start(0)
    i2c.address(0, 0x68, i2c.RECEIVER)
    local c = i2c.read(0, 7)
    i2c.stop(0)

    return to_decimal(string.byte(c, 1)), -- second
           to_decimal(string.byte(c, 2)), -- minute
           to_decimal(string.byte(c, 3)), -- hour
           to_decimal(string.byte(c, 4)), -- day of week
           to_decimal(string.byte(c, 5)), -- day of month
           to_decimal(string.byte(c, 6)), -- month
           to_decimal(string.byte(c, 7)) -- year
end

function get_time_iso_8601()
    -- see: https://en.wikipedia.org/wiki/ISO_8601
    -- example: 2015-09-08T01:55:28+00:00
    second, minute, hour, day_of_week, day_of_month, month, year = get_time()
    return string.format("20%s-%s-%s-T%s:%s:%s-03:00", year, month, day_of_month, hour, minute, second)
end

function set_time(hour, minute, second, day_of_week, date, month, year)
    i2c.start(0)
    i2c.address(0, 0x68, i2c.TRANSMITTER)
    i2c.write(0, 0x00) -- set DS3231 register pointer to 00h
    i2c.write(0, to_bcd(second))
    i2c.write(0, to_bcd(minute))
    i2c.write(0, to_bcd(hour))
    i2c.write(0, to_bcd(day_of_week))
    i2c.write(0, to_bcd(date))
    i2c.write(0, to_bcd(month))
    i2c.write(0, to_bcd(year))
    i2c.stop(0)
end

gpio_setup()
i2c_setup()
mqtt_client = mqtt_setup()
wifi_setup()

-- Examples RTC
-- set_time(10, 36, 0, 6, 4, 9, 15)
-- print(get_time_iso_8601())
