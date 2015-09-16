local logger = require "logger"

local mq = {}
local is_connected = false

local MQTT_ADDRESS = "tcc.alexandrevicenzi.com"
local MQTT_PORT = 1883
local MQTT_AUTH_USER = "guest"
local MQTT_AUTH_PWD = "guest"
local MQTT_TIMEOUT = 120

mq.on_connect = nil
mq.on_disconnect = nil
mq.is_connected = false
mq._client = nil

function mq.setup()
    logger.i("MQTT: Setup.")

    mq._client = mqtt.Client("soressa", MQTT_TIMEOUT, MQTT_AUTH_USER, MQTT_AUTH_PWD)
    mq._client:lwt("/lwt", "offline", 0, 0)

    mq._client:on("offline", function (cli)
        logger.i("MQTT: Client Offline!")
        mq.is_connected = false

        if mq.on_disconnect then
            mq.on_disconnect()
        end
    end)
end

function mq.connect()
    if mq._client then
        mq._client:connect(MQTT_ADDRESS, MQTT_PORT, 0, function (cli)
            mq.is_connected = true

            logger.i("MQTT: Connected to Broker.")

            if mq.on_connect then
                mq.on_connect(cli)
            end
        end)
    end
end

function mq.subscribe(channel)
    if mq._client and mq.is_connected then
        mq._client:subscribe(channel, 0, function (cli)
            logger.i("MQTT: Subscribed to channel.")
        end)
    end
end

function mq.publish(channel, msg)
    if mq._client and mq.is_connected then
        mq._client:publish(channel, msg, 0, 0, function (cli)
            logger.i("MQTT: Message sent.")
        end)
    end
end

function mq.disconnect()
    if mq._client and mq.is_connected then
        mq._client:close()
        logger.i("MQTT: Disconnected.")
    end
end

return mq
