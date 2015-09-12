local logger = {}

function logger.i (...)
    print("INFO", ...)
end

function logger.w (...)
    print("WARNING", ...)
end

function logger.e (...)
    print("ERROR", ...)
end

function logger.d (...)
    print("DEBUG", ...)
end

return logger
