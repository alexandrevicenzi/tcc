local rtc = {}

local function to_decimal(value)
    local hl = bit.rshift(value, 4)
    local hh = bit.band(value, 0xf)
    local hr = string.format("%d%d", hl, hh)
    return string.format("%d%d", hl, hh)
end

local function to_bcd(value)
    local d = string.format("%d", tonumber(value / 10))
    local d1 = tonumber(d * 10)
    local d2 = value - d1
    return tonumber(d * 16 + d2)
end

function rtc.setup()
    i2c.setup(0, 6, 7, i2c.SLOW)
end

function rtc.get_time()
    i2c.start(0)
    i2c.address(0, 0x68, i2c.TRANSMITTER)
    i2c.write(0, 0x00) -- set DS3231 register pointer to 00h
    i2c.stop(0)

    i2c.start(0)
    i2c.address(0, 0x68, i2c.RECEIVER)
    local c = i2c.read(0, 7)
    i2c.stop(0)

    return to_decimal(string.byte(c, 1)), -- second
           to_decimal(string.byte(c, 2)), -- minute
           to_decimal(string.byte(c, 3)), -- hour
           to_decimal(string.byte(c, 4)), -- day of week
           to_decimal(string.byte(c, 5)), -- day of month
           to_decimal(string.byte(c, 6)), -- month
           to_decimal(string.byte(c, 7)) -- year
end

function rtc.get_time_iso_8601()
    -- see: https://en.wikipedia.org/wiki/ISO_8601
    -- example: 2015-09-08T01:55:28+00:00
    second, minute, hour, day_of_week, day_of_month, month, year = rtc.get_time()
    return string.format("20%s-%s-%s-T%s:%s:%s-03:00", year, month, day_of_month, hour, minute, second)
end

function rtc.set_time(hour, minute, second, day_of_week, date, month, year)
    i2c.start(0)
    i2c.address(0, 0x68, i2c.TRANSMITTER)
    i2c.write(0, 0x00) -- set DS3231 register pointer to 00h
    i2c.write(0, to_bcd(second))
    i2c.write(0, to_bcd(minute))
    i2c.write(0, to_bcd(hour))
    i2c.write(0, to_bcd(day_of_week))
    i2c.write(0, to_bcd(date))
    i2c.write(0, to_bcd(month))
    i2c.write(0, to_bcd(year))
    i2c.stop(0)
end

return rtc
