MQTT_ADDRESS = "tcc.alexandrevicenzi.com"
MQTT_PORT = 1883
MQTT_AUTH_USER = "guest"
MQTT_AUTH_PWD = "guest"
MQTT_TIMEOUT = 120

C_TMR = 0

function wifi_connecting()
    gpio.write(1, gpio.LOW)
    gpio.write(2, gpio.LOW)

    state = false

    tmr.alarm(C_TMR, 120, 1, function()
        if (state) then
            gpio.write(1, gpio.HIGH)
        else
            gpio.write(1, gpio.LOW)
        end
        state = not state
    end)
end

function wifi_connected()
    tmr.stop(C_TMR)
    gpio.write(1, gpio.HIGH)
    gpio.write(2, gpio.LOW)
end

function wifi_error()
    tmr.stop(C_TMR)
    gpio.write(1, gpio.LOW)
    gpio.write(2, gpio.HIGH)
end

function gpio_setup()
    gpio.mode(1, gpio.OUTPUT)
    gpio.mode(2, gpio.OUTPUT)
    gpio.write(1, gpio.LOW)
    gpio.write(2, gpio.LOW)
end

function wifi_setup()
    wifi.sta.eventMonReg(wifi.STA_IDLE, function()
        print("Idle.")
        wifi.sta.connect()
    end)

    wifi.sta.eventMonReg(wifi.STA_WRONGPWD, function()
        wifi_error()
        print("Wrong password!")
    end)

    wifi.sta.eventMonReg(wifi.STA_APNOTFOUND, function()
        wifi_error()
        print("No AP found!")
    end)

    wifi.sta.eventMonReg(wifi.STA_FAIL, function()
        wifi_error()
        print("Fail!")
    end)

    wifi.sta.eventMonReg(wifi.STA_GOTIP, function()
        wifi_connected()
        ip = wifi.sta.getip()
        print("Connected. Got IP: " .. ip)
    end)

    wifi.sta.eventMonReg(wifi.STA_CONNECTING, function(prevState)
        wifi_connecting()
        if (prevState == wifi.STA_GOTIP) then
            print("Connection Lost. Attempting to reconnect...")
        else
            print("Connecting...")
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

    file.close()
end

function mqtt_setup()
    m = mqtt.Client("soressa", MQTT_TIMEOUT, MQTT_AUTH_USER, MQTT_AUTH_PWD)
    m:lwt("/lwt", "offline", 0, 0)

    m:on("connect", function(cli)
        print ("Connected to MQTT Broker.")

        cli:subscribe("/locator", 0, function(cli)
            print("subscribed")
        end)
    end)

    m:on("offline", function(cli)
        print ("MQTT Client Offline!")
    end)

    m:connect(MQTT_ADDRESS, MQTT_PORT, 0, function(cli)
        print("connected")
    end)

    --m:publish("/locator", "hello", 0, 0, function(conn) print("sent") end)

    return m
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

-- Examples RTC
-- set_time(10, 36, 0, 6, 4, 9, 15)
-- s, m, h, d, dt, mn, y = get_time()
-- print(string.format("%s/%s/20%s", dt, mn, y))
-- print(string.format("%s:%s:%s", h, m, s))

gpio_setup()
i2c_setup()
wifi_setup()
mqtt_setup()
