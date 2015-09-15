local gps = require "gps"
local led = require "led"
local logger = require "logger"
local mq = require "mq"
local network = require "network"
local rtc = require "rtc"

network.on_connect = function (ip)
    led.wifi_connected()
    mq.connect()
end

network.on_connecting = function (ip)
    led.wifi_connecting()
end

network.on_disconnect = function ()
    mq.disconnect()
end

network.on_error = function (error)
    led.wifi_error()
    mq.disconnect()
end

mq.on_connect = function (client)
    mq.subscribe("/location")
    mq.publish("/location", "test message!!!")
end

mq.on_disconnect = function ()
end

gps.on_data_received = function (data)
    if network.is_connected and mq.is_connected then
        time = rtc.get_time_iso_8601()
        bus_id = "AAA1234" -- TODO
        msg = string.format("%s,$s,%s", data, time, bus_id)
        mq.publish("/location", msg)
    end
end

led.setup()
rtc.setup()
gps.setup()
mq.setup()
-- network trigger almost all events
-- it's good to put everything before.
network.setup()
