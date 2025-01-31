import logging


COLOR_CODES = {
    "DEBUG": "\033[36m",      # Cyan
    "INFO": "\033[32m",       # Verde
    "WARNING": "\033[33m",    # Amarillo
    "ERROR": "\033[31m",      # Rojo
    "CRITICAL": "\033[35m",   # Magenta
    "RESET": "\033[0m"        # Reset color
}


class ANSIColorFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLOR_CODES.get(record.levelname, COLOR_CODES["RESET"])
        log_message = super().format(record)
        return f"{log_color}{log_message}{COLOR_CODES['RESET']}"


def setup_logger(name=__name__, level=logging.DEBUG, log_to_terminal=True, log_to_file=False, filename='project.log'):
    logger = logging.getLogger(__name__)

    handlers = []
    console_handler = None
    file_handler = None

    if log_to_terminal:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ANSIColorFormatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s"))
        handlers.append(console_handler)

    if log_to_file:
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s"))
        handlers.append(file_handler)

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        handlers=handlers
    )

    return logger
