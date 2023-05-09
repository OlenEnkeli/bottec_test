import asyncio
import logging
import logging.config

import coloredlogs

from app.core.config import LOG_CONFIG
from app.services.currency_update import CurrencyUpdate


if __name__ == '__main__':
    coloredlogs.install()
    logging.config.dictConfig(LOG_CONFIG)
    asyncio.run(CurrencyUpdate.run())
