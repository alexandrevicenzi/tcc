local logger = {}

logger.enabled = true

function logger.i (...)
    if logger.enabled then
        print("INFO", ...)
    end
end

function logger.w (...)
    if logger.enabled then
        print("WARNING", ...)
    end
end

function logger.e (...)
    if logger.enabled then
        print("ERROR", ...)
    end
end

function logger.d (...)
    if logger.enabled then
        print("DEBUG", ...)
    end
end

return logger
