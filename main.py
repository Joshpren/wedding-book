import os
import logging
from WeddingBook import WeddingBook

logger = logging.getLogger(__name__)



def setup_logging():
    # Definiere den Dateipfad
    file_path = "logging/weddingbook.log"

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


try:
    setup_logging()
    wb = WeddingBook()
    # run_by = input("Run by: \n [1] Keyboard Input \n [2] Circuit Input \n Enter 1 or 2.")
    # if run_by == '1':
    wb.run_by_keyboard_input()
    # elif run_by == '2':
    # wb.run_by_circuit_input()
    # else:
    #     print("No valid input. Program has been stopped!")


except KeyboardInterrupt:
    logger.info("Has been stopped by user!")
except Exception as e:    
    logger.exception('Got exception on main handler')
    # GPIO.cleanup()