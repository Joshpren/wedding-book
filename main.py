import os
import platform
import logging
import json
from WeddingBook import WeddingBook

logger = logging.getLogger(__name__)


def load_config():
    with open('config/config.json', 'r') as openfile:
        return json.load(openfile)


def setup_logging():
    # Definiere den Dateipfad
    system_os = platform.system()
    if system_os == "Windows":
        file_path = "var/log/wedding-book.log"
    else:
        file_path = "/var/log/wedding-book.log"

    # Extrahiere das Verzeichnis aus dem Dateipfad
    log_directory = os.path.dirname(file_path)

    # Überprüfe, ob das Verzeichnis existiert, und erstelle es, wenn nicht
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Überprüfe, ob die Datei bereits existiert
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            print("")
            # logger.info(f"Die Datei {file_path} wurde erstellt.")
           
    logging.basicConfig(filename=file_path, level=logging.DEBUG, filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S',)
    log_init = """
                    #     #                                      ######                       
                    #  #  # ###### #####  #####  # #    #  ####  #     #  ####   ####  #    # 
                    #  #  # #      #    # #    # # ##   # #    # #     # #    # #    # #   #  
                    #  #  # #####  #    # #    # # # #  # #      ######  #    # #    # ####   
                    #  #  # #      #    # #    # # #  # # #  ### #     # #    # #    # #  #   
                    #  #  # #      #    # #    # # #   ## #    # #     # #    # #    # #   #  
                    ## ##  ###### #####  #####  # #    #  ####  ######   ####   ####  #    # is starting!                                                                       
                    """
    logger.info(log_init)
    logger.info(f"Project-Directory: {os.path.dirname(os.path.realpath(__file__))}")


try:
    setup_logging()
    config = load_config()
    wb = WeddingBook()
    
    wb.gpio_setup()
    wb.run_by_circuit_input()



except KeyboardInterrupt:
    logger.info("Has been stopped by KeyboardInterrupt.")
except Exception as e:    
    logger.exception('Got exception on main handler')
# wb.gpio_cleanup()