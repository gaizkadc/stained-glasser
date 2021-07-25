import os
import sys
import logging
from logging.handlers import RotatingFileHandler


def get_logger():
    logs_folder_path = os.getenv('LOGS_FOLDER_PATH')
    app_name = os.getenv('APP_NAME')

    if not os.path.isdir(logs_folder_path):
        os.mkdir(logs_folder_path)
    log_file_path = logs_folder_path + '/' + app_name + '.log'
    if not os.path.isfile(log_file_path):
        log_file = open(log_file_path, "a")
        log_file.close()

    logger = logging.getLogger(app_name)
    logger.setLevel('DEBUG')

    log_format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(log_file_path, maxBytes=(1048576 * 5), backupCount=5)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    logger.info('logger created')

    return logger


def create_output_folder(logger, today):
    logger.info('creating output folder')

    output_folder_path = os.getenv('OUTPUT_FOLDER_PATH')

    output_folder_path = output_folder_path + '/' + today

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    else:
        file_list = [f for f in os.listdir(output_folder_path)]
        for file in file_list:
            os.remove(os.path.join(output_folder_path, file))

    return output_folder_path
