local led = {}

local led_state = false

local WIFI_OK_LED = 1 -- pin 1 (GPIO 5)
local WIFI_ERROR_LED = 2 -- pin 2 (GPIO 4)
local WIFI_TMR = 0

function led.setup()
    gpio.mode(WIFI_OK_LED, gpio.OUTPUT)
    gpio.mode(WIFI_ERROR_LED, gpio.OUTPUT)
    gpio.write(WIFI_OK_LED, gpio.LOW)
    gpio.write(WIFI_ERROR_LED, gpio.LOW)
end

function led.wifi_connecting()
    gpio.write(WIFI_OK_LED, gpio.LOW)
    gpio.write(WIFI_ERROR_LED, gpio.LOW)

    tmr.alarm(WIFI_TMR, 120, 1, function()
        tmr.wdclr()

        if (led_state) then
            gpio.write(WIFI_OK_LED, gpio.HIGH)
        else
            gpio.write(WIFI_OK_LED, gpio.LOW)
        end
        led_state = not led_state
    end)
end

function led.wifi_connected()
    tmr.stop(WIFI_TMR)
    gpio.write(WIFI_OK_LED, gpio.HIGH)
    gpio.write(WIFI_ERROR_LED, gpio.LOW)
end

function led.wifi_error()
    tmr.stop(WIFI_TMR)
    gpio.write(WIFI_OK_LED, gpio.LOW)
    gpio.write(WIFI_ERROR_LED, gpio.HIGH)
end

return led
