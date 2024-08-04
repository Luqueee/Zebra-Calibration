import requests
import json
import threading
import os
import subprocess
import xml.dom.minidom as md 
import time
import socket
import datetime
import psutil

start = time.time()
LOGS_FOLDER = r'C:\Program files (x86)\TreHoffman Technologies\RAW Print\Logs'

def timestamp():
    return f"{datetime.datetime.now()} {socket.gethostname()}"

def timestamp_log():
    name = f"{datetime.datetime.now()}"
    name = name.replace(" ","_")
    name = name.replace(".","-")
    name = name.replace(":","-")
    name += socket.gethostname()
    print(name)
    return name + ".txt"

def CreateLog(error):
    folderExist = os.path.exists(LOGS_FOLDER)
    if not folderExist:
        os.makedirs(LOGS_FOLDER)
    with open(os.path.join(LOGS_FOLDER,timestamp_log()), "w") as log:
        log.write(str(error))

def process_status(process_name):
    count = 0
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            count += 1
    return count

PRINTNAME_PATH = r'C:\Program files (x86)\TreHoffman Technologies\RAW Print\PrinterName.txt'
ACTIVITY_PATH = r'C:\Program files (x86)\TreHoffman Technologies\RAW Print\Activity.txt'
PROGRAMOPTIONS_PATH = r'C:\Program files (x86)\TreHoffman Technologies\RAW Print\ProgramOptions.json'
SPOOL_PATH = r"C:\Windows\System32\spool\PRINTERS"


try:
    if process_status("Calibrar_Zebra.exe") <= 2:

        RAWPRINT_PATH = r"C:\Program files (x86)\TreHoffman Technologies\RAW Print\RawPrint.exe.config"
        FILE_RAW = md.parse(RAWPRINT_PATH)
        IP_RAW = FILE_RAW.getElementsByTagName("add")[0].getAttribute("value")
        PORT_RAW = FILE_RAW.getElementsByTagName("add")[1].getAttribute("value")
        
    
    
        try:
            with open(PRINTNAME_PATH, "r") as FILE_RAW:
                PRINTERNAME = FILE_RAW.readline()
        except FileNotFoundError:
            with open(PRINTNAME_PATH, "w") as FILE_RAW:
                FILE_RAW.write("Zebra ETC")
                FILE_RAW.close()
                PRINTERNAME = "Zebra ETC"


        try:
            with open(PROGRAMOPTIONS_PATH, "r") as JSON_FILE:
                OPTIONS = json.load(JSON_FILE)
        except FileNotFoundError:
            with open(PROGRAMOPTIONS_PATH, "w") as JSON_FILE:
                OPTIONS = {
                    "OPTIONS": {
                        "PRINT_OUTPUT": False
                    },
                    "EXECUTION OPTIONS": {
                        "RESET SPOOLER": True,
                        "RESET RAWPRINT": True,
                        "ASK PRINTER ON ERROR": False
                    }
                }
                json.dump(OPTIONS, JSON_FILE, indent=4)

        PRINT_OUTPUT = OPTIONS["OPTIONS"]["PRINT_OUTPUT"]
        RESET_SPOOLER = OPTIONS["EXECUTION OPTIONS"]["RESET SPOOLER"]
        RESET_RAWPRINT = OPTIONS["EXECUTION OPTIONS"]["RESET RAWPRINT"]
        ASK_PRINTER_ON_ERROR = OPTIONS["EXECUTION OPTIONS"]["ASK PRINTER ON ERROR"]

        def RunCommand(command):
            if PRINT_OUTPUT == False:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.run(command,  stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=False, startupinfo=si)
            else:
                subprocess.run(command)

        def FindPrinter():
            req = requests.get(f"{IP_RAW}:{PORT_RAW}")
            res = req.json()
            for element in res:
                if element["Name"] == PRINTERNAME:
                    return element
            return None

        def main():
           
            def PrintContext(text):
                if PRINT_OUTPUT:
                    print(text)
                
            def Spooler():
                RunCommand('net stop "Servicio LPD"')
                RunCommand("net stop spooler")
                
                for el in os.listdir(SPOOL_PATH):   
                    os.remove(os.path.join(SPOOL_PATH,el))
                    
                RunCommand('net start "Servicio LPD"')
                RunCommand("net start spooler")

                PrintContext("Ficheros temporales eliminados con exito")

            def RawPrint():
                RunCommand('net stop "RAW Print"')
                RunCommand('net start "RAW Print"')

            threads = list()
            PrintContext("Ejecutando procesos de verificacion...")
            if RESET_SPOOLER:
                spooler = threading.Thread(target=Spooler, daemon=True)
                spooler.start()
                threads.append(spooler)
            if RESET_RAWPRINT:
                rawprint = threading.Thread(target=RawPrint, daemon=True)
                rawprint.start()
                threads.append(rawprint)

            for index, thread in enumerate(threads):
                thread.join()

            SEND = True

            if SEND:
                REQURL = f"{IP_RAW}:{PORT_RAW}"
                PAYLOAD = json.dumps({
                "printer": PRINTERNAME,
                "data": "^XA~JC^XZ"
                })
                requests.request("POST", REQURL, data=PAYLOAD)

            PrintContext("Calibracion enviada con exito.")    
            
            try:
                with open(ACTIVITY_PATH, "a") as ACTIVITY_FILE:
                    ACTIVITY_FILE.write(f"\n{timestamp()}")
                    
            except FileNotFoundError:
                with open(ACTIVITY_FILE, "w") as ACTIVITY_FILE:
                    ACTIVITY_FILE.write("")


    
        printer = FindPrinter()
        print(printer)

        if printer != None:
            try:
                main()
                end = time.time()
                print(f"Total time execution: {round(end-start,2)}")
                if PRINT_OUTPUT == True:
                    input(".....")
            except Exception as e:
                CreateLog(e)
                
        else:

                try:
                    with open(ACTIVITY_PATH, "a") as ACTIVITY_FILE:
                        ACTIVITY_FILE.write(f"\n{timestamp()} No se encontro la impresora {PRINTERNAME}")
                            
                except FileNotFoundError:
                    with open(ACTIVITY_FILE, "w") as ACTIVITY_FILE:
                        ACTIVITY_FILE.write("")
            
                if ASK_PRINTER_ON_ERROR == True:
                
                    import customtkinter
                    PRINTNAME_PATH = r'C:\Program files (x86)\TreHoffman Technologies\RAW Print\PrinterName.txt'
                    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
                    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

                    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
                    app.geometry("400x240")

                    def button_function():
                        with open(PRINTNAME_PATH, "w") as FILE_RAW:
                            FILE_RAW.write(printername.get())
                            FILE_RAW.close()
                        app.destroy()
                        main()
                        exit(1)
                        
                    printername = customtkinter.CTkEntry(master=app,
                                                placeholder_text="Nombre de la impresora. Defecte: Zebra ETC",
                                                width=280,
                                                height=35,
                                                corner_radius=10)
                    printername.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)
                    button = customtkinter.CTkButton(master=app, text="Cambiar nombre", command=button_function)
                    button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
                    app.mainloop()
except Exception as e:
    CreateLog(e)    