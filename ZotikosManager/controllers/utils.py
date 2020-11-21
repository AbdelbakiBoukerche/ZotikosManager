from datetime import datetime


def log_console(output):
    print(f"{str(datetime.now())[:-3]}: {output}")

