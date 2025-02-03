import logging

logger = logging.getLogger(__name__)


class StateHandler:
    def __init__(self):
        self.states = {}
        logger.debug("StateManager inicializado.")

    def register(self, key: str, initial_value=None):
        if key not in self.states:
            self.states[key] = {
                'value': initial_value,
                'subscribers': []
            }
            logger.debug(f"Estado registrado: '{key}' con valor inicial: {initial_value}")
        else:
            # self.set(key, initial_value)
            logger.warning(f"Intento de registrar un estado existente: '{key}'")

    def subscribe(self, key: str, callback, value=None):
        self.register(key=key, initial_value=value)
        self.states[key]['subscribers'].append(callback)
        logger.debug(f"Suscriptor añadido al estado: '{key}'")

    def get(self, key: str):
        value = self.states.get(key, {}).get('value', None)
        if value is None:
            logger.warning(f"Intento de obtener un estado no registrado: '{key}'")
        else:
            logger.debug(f"Valor obtenido para el estado '{key}': {value}")
        return value

    def set(self, key: str, value):
        if key not in self.states:
            self.register(key, value)
            logger.info(f"Estado no registrado previamente. Registrado automáticamente: '{key}'")
        old_value = self.states[key]['value']
        self.states[key]['value'] = value
        logger.info(f"Estado actualizado: '{key}' de '{old_value}' a '{value}'")
        self._notify(key, value)

    def _notify(self, key: str, value):
        subscribers = self.states.get(key, {}).get('subscribers', [])
        if not subscribers:
            logger.warning(f"No hay suscriptores para el estado: '{key}'")
        for callback in subscribers:
            try:
                callback(key, value)
                logger.debug(f"Suscriptor notificado para el estado '{key}' con valor: {value}")
            except Exception as e:
                logger.error(f"Error notificando al suscriptor en la clave '{key}': {e}")
