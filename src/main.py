import logging

from flet import Page, app
from flet.core.types import AppView

try:
    from utils.logger import setup_logger
    from managers.app_manager import AppManager
except:
    from utils.logger import setup_logger
    from managers.app_manager import AppManager

logger = setup_logger(__name__, level=logging.DEBUG, log_to_file=False)


def main(page: Page):
    logger.info("Initializing the application")
    app_manager = AppManager()
    app_manager.page = page
    app_manager.initialize_app()
    logger.info("Application initialized successfully")


if __name__ == "__main__":
    app(
        target=main,
        assets_dir="assets",
        view=AppView.WEB_BROWSER,
        port=8000,
        host="127.0.0.1"
    )
