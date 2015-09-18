local led_state = false

local WIFI_OK_LED = 1 -- pin 1 (GPIO 5)
local WIFI_ERROR_LED = 2 -- pin 2 (GPIO 4)
local MQTT_LED = 3 -- TODO

local function setup()
    gpio.mode(WIFI_OK_LED, gpio.OUTPUT)
    gpio.mode(WIFI_ERROR_LED, gpio.OUTPUT)
    gpio.mode(MQTT_LED, gpio.OUTPUT)
    gpio.write(WIFI_OK_LED, gpio.LOW)
    gpio.write(WIFI_ERROR_LED, gpio.LOW)
    gpio.write(MQTT_LED, gpio.LOW)
end

local function start_blink(led)
    gpio.write(led, gpio.LOW)

    tmr.alarm(0, 120, 1, function()
        tmr.wdclr()

        if (led_state) then
            gpio.write(led, gpio.HIGH)
        else
            gpio.write(led, gpio.LOW)
        end
        led_state = not led_state
    end)
end

local function stop_blink()
    tmr.stop(0)
end

local function on(led)
    gpio.write(led, gpio.HIGH)
end

local function off(led)
    gpio.write(led, gpio.LOW)
end

return {
    setup = setup,
    start_blink = start_blink,
    stop_blink = stop_blink,
    on = on,
    off = off,
    WIFI_OK = WIFI_OK_LED,
    WIFI_ERROR = WIFI_ERROR_LED,
    MQTT = MQTT_LED,
}
