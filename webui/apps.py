from django.apps import AppConfig


class WebuiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webui'
    module = 'WeddingBook'


    def ready(self):
        from webui import WeddingBook
        wb = WeddingBook.WeddingBook()
        try:
            # setup_logging()
            wb.run_by_circuit_input()
            # run_by = input("Run by: \n [1] Keyboard Input \n [2] Circuit Input \n Enter 1 or 2.")
            # if run_by == '1':
            #     wb.run_by_keyboard_input()
            # elif run_by == '2':
            #     wb.run_by_circuit_input()
            # else:
            #     print("No valid input. Program has been stopped!")


        except:
            GPIO.cleanup()
