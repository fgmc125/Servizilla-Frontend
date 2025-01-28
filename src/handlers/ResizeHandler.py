import logging


class ResizeHandler:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Initializing MediaQuery")
        self._subscribers = []

    def subscribe(self, func):
        if callable(func):
            self._subscribers.append(func)

    def unsubscribe(self, func):
        self._subscribers = [f for f in self._subscribers if f is not func]

    def on_resized(self, event):
        new_size = (event.control.width, event.control.height)
        print(new_size)
        for func in self._subscribers:
            try:
                func(new_size)
            except Exception as e:
                self.logger.info(f"Error al ejecutar la función suscrita: {e}")
