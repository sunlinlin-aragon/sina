from django.conf import settings
import logging


def get_file_logger(name, format='%(asctime)s %(levelname)s\n%(message)s\n', level=logging.DEBUG):
    log = logging.getLogger(name)
    if not log.handlers:
        handler = logging.FileHandler('%s/logs/%s.log' % (settings.PROJECT_ROOT, name))
        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel(level)
    return log