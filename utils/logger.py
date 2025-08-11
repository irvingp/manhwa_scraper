import logging

def get_logger(name="manhwa_scraper"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler("scraper.log", encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger