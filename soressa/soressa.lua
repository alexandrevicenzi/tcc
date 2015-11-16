local led = require "led"
local time = require "time"

local mq
local notify = false
local queue = {}
local DEVICE_ID = wifi.sta.getmac()
local on_wifi = wifi.sta.eventMonReg
local shift = table.remove

function gps_on()
    led.on(led.GPS)
    gpio.write(4, gpio.LOW)

    tmr.alarm(3, 10000, 0, function ()
        tmr.wdclr()
        gps_off(true)
    end)
end

function gps_off(autoreload)
    led.off(led.GPS)
    gpio.write(4, gpio.HIGH)

    if autoreload then
        tmr.alarm(2, 30000, 0, function ()
            tmr.wdclr()
            gps_on()
        end)
    end
end

local function stop_events()
    gps_off(false)
    uart.on("data")
    led.off(led.MQTT)
    --if mq then mq:close() end
end

local function wifi_err(...)
    print("Wifi error! Reconnecting in 5 sec.")
    stop_events()
    led.stop_blink()
    led.off(led.WIFI)
    led.on(led.ERROR)

    tmr.alarm(1, 5000, 0, function ()
        tmr.wdclr()
        wifi.sta.connect()
    end)
end

local function publish(channel, msg)
    if is_sending then
        queue[#queue + 1] = { channel, msg }
    else
        is_sending = true

        mq:publish(channel, msg, 0, 0, function (cli)
            print("Message sent to ".. channel)
            is_sending = false

            tmr.wdclr()
            print("Heap: " .. node.heap())

            if #queue > 0 then
                item = shift(queue, 1)
                publish(item[1], item[2])
            end
        end)
    end
end

local function send_data(channel, data)
    local ts = time.time()
    local msg = string.format("{\"data\":\"%s\",\"ts\":\"%s\",\"id\":\"%s\"}", data, ts, DEVICE_ID)
    publish(channel, msg)
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
            ssid, pwd, bssid = string.match(line, "([^,]+),([^,]+),([^,]+)\n")
            wifi.sta.config(ssid, pwd, 1, bssid)
            line = file.readline()
        end

        file.close()
    end
end

function start_all()
    mq:connect("tcc.alexandrevicenzi.com", 1883, 0, function ()
        print("MQTT connected.")
        led.on(led.MQTT)

        uart.on("data", "\n", function (data)
            if (string.sub(data, 1, 1) == "$") then
                local sentence = string.sub(data, 2, 6)

                if sentence == "GPGLL" or
                   sentence == "GPGGA" or
                   sentence == "GPRMC" or
                   sentence == "GPVTG"
                then
                    send_data("/gpslocation", string.sub(data, 1, string.len(data) - 2))
                end
            end
        end, 0)

        if notify then
            notify = false
            wifi.sta.getap(1, scan_ap)
        end

        gps_on()
    end)
end

gpio.mode(4, gpio.OUTPUT)
led.setup()
time.setup()

mq = mqtt.Client("soressa", 60, "guest", "guest")
mq:lwt("/lwt", "offline", 0, 0)
mq:on("offline", function ()
    stop_events()
    print("MQTT Offine!")

    if wifi.sta.status() == wifi.STA_GOTIP then
        start_all()
    end
end)

on_wifi(wifi.STA_WRONGPWD, wifi_err)
on_wifi(wifi.STA_APNOTFOUND, wifi_err)
on_wifi(wifi.STA_FAIL, wifi_err)
on_wifi(wifi.STA_IDLE, function () wifi.sta.connect() end)

on_wifi(wifi.STA_GOTIP, function ()
    print("Wifi connected.")
    led.off(led.ERROR)
    led.stop_blink()
    led.on(led.WIFI)
    notify = true
    start_all()
end)

on_wifi(wifi.STA_CONNECTING, function ()
    print("Wifi connecting...")
    stop_events()
    led.off(led.ERROR)
    led.start_blink(led.WIFI)
end)

wifi.sta.eventMonStart()
wifi.setmode(wifi.STATION)
wifi.sta.autoconnect(1)
load_ap()
