-- WIFI

wifi.setmode(wifi.STATION)
wifi.sta.config("ap111 2.0", "alexandrede1a9")
wifi.sta.connect()
print(wifi.sta.getip())

-- MQTT
m = mqtt.Client("soressa", 120, "guest", "guest")
m:lwt("/lwt", "offline", 0, 0)

m:on("connect", function(con) print ("connected") end)
m:on("offline", function(con) print ("offline") end)
m:on("message", function(conn, topic, data)
  print(topic .. ":" ) 
  if data ~= nil then
    print(data)
  end
end)

m:connect("192.168.81.1", 1883, 0, function(conn) print("connected") end)
m:subscribe("/locator", 0, function(conn) print("subscribed") end)
m:publish("/locator", "hello", 0, 0, function(conn) print("sent") end)
m:close();
