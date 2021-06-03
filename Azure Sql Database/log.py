import logging

def logger(text):
    
    log=logging.getLogger(__name__)
    logging.basicConfig(filename='logging.log',level=logging.INFO,format='%(levelname)s :%(name)s: %(asctime)s: %(message)s')
    log.info(text)