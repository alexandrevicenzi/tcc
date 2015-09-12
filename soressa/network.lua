local logger = require "logger"

local network = {}

local function wifi_error(error)
    if network.on_error ~= nil then
        network.on_error(error)
    end
end

function network.setup()
    wifi.sta.eventMonReg(wifi.STA_IDLE, function()
        logger.i("WIFI: Idle.")
        wifi.sta.connect()
    end)

    wifi.sta.eventMonReg(wifi.STA_WRONGPWD, function()
        logger.e("WIFI: Wrong password!")
        wifi_error(wifi.STA_WRONGPWD)
    end)

    wifi.sta.eventMonReg(wifi.STA_APNOTFOUND, function()
        logger.e("WIFI: No AP found!")
        wifi_error(wifi.STA_APNOTFOUND)
    end)

    wifi.sta.eventMonReg(wifi.STA_FAIL, function()
        logger.e("WIFI: Fail!")
        wifi_error(wifi.STA_FAIL)
    end)

    wifi.sta.eventMonReg(wifi.STA_GOTIP, function()
        ip = wifi.sta.getip()
        logger.i("WIFI: Connected. Got IP: " .. ip)

        if network.on_connect ~= nil then
            network.on_connect(ip)
        end
    end)

    wifi.sta.eventMonReg(wifi.STA_CONNECTING, function(prev_state)
        if (prev_state == wifi.STA_GOTIP) then
            logger.i("WIFI: Connection Lost. Attempting to reconnect...")

            if network.on_disconnect ~= nil then
                network.on_disconnect()
            end
        else
            logger.i("WIFI: Connecting...")
        end

        if network.on_connecting ~= nil then
            network.on_connecting()
        end
    end)

    wifi.sta.eventMonStart()

    wifi.setmode(wifi.STATION)
    wifi.sta.autoconnect(1)

    wifi.sta.config("ssid", "pwd")
end

function network.is_connected()
    return wifi.sta.status() == wifi.STA_GOTIP
end

network.on_connect = nil
network.on_connecting = nil
network.on_disconnect = nil
network.on_error = nil

return network
