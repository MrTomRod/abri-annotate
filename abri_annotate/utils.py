import logging

logger = logging.getLogger("ABRicate")


def init_logfile(genome_identifier, logfile):
    assert genome_identifier is not None, f'Could not set up logging: genome_identifier is undefined!'

    # remove pre-existing handlers
    logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s | %(name)s |  %(levelname)s: %(message)s')
    logger.setLevel(logging.DEBUG)

    # log to STDOUT
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # log to logfile
    file_handler = logging.FileHandler(filename=logfile)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
