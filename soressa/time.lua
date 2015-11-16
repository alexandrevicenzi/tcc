local function to_decimal(value)
    local hl = bit.rshift(value, 4)
    local hh = bit.band(value, 0xf)
    return string.format("%d%d", hl, hh)
end

local function setup()
    i2c.setup(0, 6, 7, i2c.SLOW)
end

local function time()
    i2c.start(0)
    i2c.address(0, 0x68, i2c.TRANSMITTER)
    i2c.write(0, 0x00)
    i2c.stop(0)

    i2c.start(0)
    i2c.address(0, 0x68, i2c.RECEIVER)
    local bytes = i2c.read(0, 7)
    i2c.stop(0)

    local second, minute, hour, day_of_week, day_of_month, month, year

    second = to_decimal(string.byte(bytes, 1))
    minute = to_decimal(string.byte(bytes, 2))
    hour = to_decimal(string.byte(bytes, 3))
    day_of_week = to_decimal(string.byte(bytes, 4))
    day_of_month = to_decimal(string.byte(bytes, 5))
    month = to_decimal(string.byte(bytes, 6))
    year = to_decimal(string.byte(bytes, 7))

    return string.format("20%s-%s-%s-T%s:%s:%s", year, month, day_of_month, hour, minute, second)
end

return {
    setup = setup,
    time = time
}
