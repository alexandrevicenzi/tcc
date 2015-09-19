node.compile("led.lua")
node.compile("time.lua")
node.compile("soressa.lua")

file.remove("led.lua")
file.remove("time.lua")
file.remove("soressa.lua")

dofile("soressa.lc")
