import logging

# create a logger with name of the file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.FileHandler("../test.log")
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

logger.info('info message')

if __name__ == '__main__':
    print("hello")