local logger = require "logger"

local mq = {}
local is_connected = false
local client = nil

local MQTT_ADDRESS = "tcc.alexandrevicenzi.com"
local MQTT_PORT = 1883
local MQTT_AUTH_USER = "guest"
local MQTT_AUTH_PWD = "guest"
local MQTT_TIMEOUT = 120

mq.on_connect = nil
mq.on_disconnect = nil

function mq.setup()
    m = mqtt.Client("soressa", MQTT_TIMEOUT, MQTT_AUTH_USER, MQTT_AUTH_PWD)
    client = m

    m:lwt("/lwt", "offline", 0, 0)

    m:on("connect", function (cli)
        logger.i("MQTT: Connected to Broker.")
        is_connected = true

        if mq.on_connect ~= nil then
            mq.on_connect(cli)
        end
    end)

    m:on("offline", function (cli)
        logger.i("MQTT: Client Offline!")
        is_connected = false

        if mq.on_disconnect ~= nil then
            mq.on_disconnect()
        end
    end)
end

function mq.connect()
    if client then
        client:connect(MQTT_ADDRESS, MQTT_PORT, 0, function (cli)
            logger.i("MQTT: Connected.")
        end)
    end
end

function mq.subscribe(channel)
    if client then
        client:subscribe(channel, 0, function (cli)
            logger.i("MQTT: Subscribed to channel.")
        end)
    end
end

function mq.publish(channel, msg)
    client:publish(channel, msg, 0, 0, function (cli)
        logger.i("MQTT: Message sent.")
    end)
end

function mq.disconnect()
    if client then
        client:close()
    end
end

function mq.is_connected()
    return is_connected
end

return mq
