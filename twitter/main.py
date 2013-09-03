import os
import sys
import bot
import logging
from logger import MonthlyRotatingFileHandler


def setup_logging():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logging.basicConfig(level=logging.INFO)
    logging_handler = MonthlyRotatingFileHandler(os.path.join(current_dir, 'logs/bot.log'))
    logging_handler.setLevel(logging.INFO)
    logging_handler.suffix = '%Y%m'
    logging_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(message)s',
        '%Y-%m-%d %H:%M:%S'
    ))
    logger = logging.getLogger('bot')
    logger.addHandler(logging_handler)


def main():
    settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), bot.SETTINGS_FILE)
    handler = bot.BotHandler(settings_file)
    handler.run()


def command(*args):
    bot.command(*args)


if __name__ == '__main__':
    setup_logging()
    try:
        if len(sys.argv) > 1:
            command(*sys.argv[1:])
        else:
            main()
    except KeyboardInterrupt:
        sys.exit(0)
