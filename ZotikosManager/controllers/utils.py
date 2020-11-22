from datetime import datetime
import spdlog as spd


CORE_LOGGER = spd.ConsoleLogger("CORE_LOGGER")
CORE_LOGGER.set_pattern("%^[%T] %n: %v%$")
CORE_LOGGER.set_level(spd.LogLevel.INFO)


def log_console(output):
    print(f"{str(datetime.now())[:-3]}: {output}")

