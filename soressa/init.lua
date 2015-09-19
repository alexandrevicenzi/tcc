local m = gpio.mode
local w = gpio.write

m(0, gpio.OUTPUT)
m(1, gpio.OUTPUT)
m(2, gpio.OUTPUT)
m(5, gpio.OUTPUT)

w(0, gpio.HIGH)
w(1, gpio.HIGH)
w(2, gpio.HIGH)
w(5, gpio.HIGH)

print("*******************************")
print("***   BOOTLOOP PROTECTION   ***")
print("*** Run halt() to quit boot ***")
print("*******************************")

function halt()
    tmr.stop(0)
end

tmr.alarm(0, 5000, 0, function()
    w(0, gpio.LOW)
    w(1, gpio.LOW)
    w(2, gpio.LOW)
    w(5, gpio.LOW)

    print("Booting...")
    dofile("soressa.lc")
end)
