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
    print("Wifi error!")
    stop_events()
    led.stop_blink()
    led.off(led.WIFI)
    led.off(led.MQTT)
    led.off(led.GPS)
    led.on(led.ERROR)

    tmr.alarm(2, 5000, 0, function ()
        tmr.wdclr()
        wifi.sta.connect()
    end)
end

local function send_data(channel, data)
    local ts = time.time()
    local msg = string.format("{\"data\":\"%s\",\"ts\":\"%s\",\"id\":\"%s\"}", data, ts, DEVICE_ID)
    mq:publish(channel, msg, 0, 0, void)
    print("Message sent to ".. channel)
end

local function scan_ap(t)
    local ssid, pwd, set, bssid = wifi.sta.getconfig()
    local c = (t[bssid])
    if c then send_data("/accesspoint", bssid.. "," ..c) end
end

local function load_ap()
    if file.open("wpa.conf", "r") then
        local line, i, j, l, ssid, pwd, bssid
        line = file.readline()

        while line ~= nil do
            i, j = string.find(line, ",", 1)
            ssid = string.sub(line, 0, i - 1)
            j, l = string.find(line, ",", i + 1)
            pwd = string.sub(line, i + 1, j - 1)
            bssid  = string.sub(line, j + 1, string.len(line) - 1)
            wifi.sta.config(ssid, pwd, 1, bssid)
            line = file.readline()
        end

        file.close()
    end
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
    print("Wifi connected.")
    led.off(led.ERROR)
    led.stop_blink()
    led.on(led.WIFI)

    mq:connect("tcc.alexandrevicenzi.com", 1883, 0, function ()
        print("MQTT connected.")
        led.on(led.MQTT)

        uart.on("data", "\n", function (data)
            if (string.sub(data, 1, 1) == "$") then
                send_data("/gpslocation", string.sub(data, 1, string.len(data) - 1))
            else
                print(data)
            end
        end, 0)

        tmr.alarm(1, 30000, 1, function ()
            tmr.wdclr()
            wifi.sta.getap(1, scan_ap)
        end)
    end)
end)

on_wifi(wifi.STA_CONNECTING, function ()
    print("Wifi connecting...")
    stop_events()
    led.off(led.ERROR)
    led.off(led.MQTT)
    led.off(led.GPS)
    led.start_blink(led.WIFI)
end)

wifi.sta.eventMonStart()

wifi.setmode(wifi.STATION)
wifi.sta.autoconnect(1)

load_ap()
