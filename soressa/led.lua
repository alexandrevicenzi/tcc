local led_state = false

local ERROR_LED = 2 -- pin 2 (GPIO 4)
local GPS_LED = 5 -- pin 5 (GPIO 14)
local MQTT_LED = 0 -- pin 0 (GPIO 16)
local WIFI_LED = 1 -- pin 1 (GPIO 5)

local function setup()
    gpio.mode(ERROR_LED, gpio.OUTPUT)
    gpio.mode(MQTT_LED, gpio.OUTPUT)
    gpio.mode(GPS_LED, gpio.OUTPUT)
    gpio.mode(WIFI_LED, gpio.OUTPUT)
    gpio.write(ERROR_LED, gpio.LOW)
    gpio.write(GPS_LED, gpio.LOW)
    gpio.write(MQTT_LED, gpio.LOW)
    gpio.write(WIFI_LED, gpio.LOW)
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
    ERROR = ERROR_LED,
    GPS = GPS_LED,
    MQTT = MQTT_LED,
    WIFI = WIFI_LED
}
