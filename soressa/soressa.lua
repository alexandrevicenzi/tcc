local led = require "led"
local time = require "time"

local mq
local DEVICE_ID = wifi.sta.getmac()
local on_wifi = wifi.sta.eventMonReg
local void = function (...) end

local function stop_events()
    uart.on("data")
    tmr.stop(1)
    if mq then mq:close() end
end

local function wifi_err(...)
    stop_events()
    led.stop_blink(led.WIFI_OK)
    led.off(led.WIFI_OK)
    led.on(led.WIFI_ERROR)

    tmr.alarm(2, 5000, 0, function ()
        tmr.wdclr()
        wifi.sta.connect()
    end)
end

local function on_ap(data)
    time = time.time()
    local msg = string.format("{\"data\":\"%s\",\"ts\":\"%s\",\"id\":\"%s\"}", data, time, DEVICE_ID)
    mq:publish("/accesspoint", msg, 0, 0, void)
end

local function on_gps(data)
    time = time.time()
    local msg = string.format("{\"data\":\"%s\",\"ts\":\"%s\",\"id\":\"%s\"}", data, time, DEVICE_ID)
    mq:publish("/gpslocation", msg, 0, 0, void)
end

local function scan_ap(t)
    ssid, pwd, set, bssid = wifi.sta.getconfig()
    ap = t[bssid]
    if ap then on_ap(bssid.. "," ..ap) end
end

led.setup()
time.setup()

mq = mqtt.Client("soressa", 120, "guest", "guest")
mq:lwt("/lwt", "offline", 0, 0)
mq:on("offline", function () led.off(led.MQTT) end)

on_wifi(wifi.STA_WRONGPWD, wifi_err)
on_wifi(wifi.STA_APNOTFOUND, wifi_err)
on_wifi(wifi.STA_FAIL, wifi_err)
on_wifi(wifi.STA_IDLE, function () wifi.sta.connect() end)

on_wifi(wifi.STA_GOTIP, function ()
    led.off(led.WIFI_ERROR)
    led.stop_blink(led.WIFI_OK)
    led.on(led.WIFI_OK)

    mq:connect("tcc.alexandrevicenzi.com", 1883, 0, function ()
        mq:subscribe("/accesspoint", 0, void)
        mq:subscribe("/gpslocation", 0, void)

        led.on(led.MQTT)

        uart.on("data", "\n", function (data)
            if (string.sub(data, 1, 1) == "$") then
                on_gps(string.sub(data, 1, string.len(data) - 1))
            else
                print(data)
            end
        end, 0)

        tmr.alarm(1, 10000, 1, function ()
            tmr.wdclr()
            wifi.sta.getap(1, scan_ap)
        end)
    end)
end)

on_wifi(wifi.STA_CONNECTING, function ()
    stop_events()
    led.off(led.WIFI_ERROR)
    led.off(led.MQTT)
    led.start_blink(led.WIFI_OK)
end)

wifi.sta.eventMonStart()

wifi.setmode(wifi.STATION)
wifi.sta.autoconnect(1)
