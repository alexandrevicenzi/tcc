local logger = require "logger"

local gps = {}

gps.on_data_received = nil

function gps.setup()
    logger.i("GPS: Setup.")
end

return gps
