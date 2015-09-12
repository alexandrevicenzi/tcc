print("*******************************")
print("***   BOOTLOOP PROTECTION   ***")
print("*** Run halt() to quit boot ***")
print("*******************************")

function halt()
    tmr.stop(0)
end

tmr.alarm(0, 5000, 0, function()
    print("Booting...")
    dofile("soressa.lc")
end)
