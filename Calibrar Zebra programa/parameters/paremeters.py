import requests
import json
import threading
import os
import subprocess
from colorama import Fore, init, just_fix_windows_console
import xml.dom.minidom as md 
import time
just_fix_windows_console()
init(autoreset=True)


start = time.time()
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

PRINTNAME_PATH = r'C:\Program files (x86)\TreHoffman Technologies\RAW Print\PrinterName.txt'
SPOOL_PATH = r"C:\Windows\System32\spool\PRINTERS"
RAWPRINT_PATH = r"C:\Program files (x86)\TreHoffman Technologies\RAW Print\RawPrint.exe.config"

FILE_RAW = md.parse(RAWPRINT_PATH)
IP_RAW = FILE_RAW.getElementsByTagName("add")[0].getAttribute("value")
PORT_RAW = FILE_RAW.getElementsByTagName("add")[1].getAttribute("value")


def Spooler():
    subprocess.run("net stop spooler", startupinfo=si)
        
    for el in os.listdir(SPOOL_PATH):   
        os.remove(os.path.join(SPOOL_PATH,el))
    subprocess.run("net start spooler", startupinfo=si)

    print(Fore.GREEN + "Ficheros temporales eliminados con exito")

def RawPrint():
    subprocess.run('net stop "RAW Print"', startupinfo=si)
    subprocess.run('net start "RAW Print"', startupinfo=si)


    
threads = list()

print(Fore.GREEN + "Ejecutando procesos de verificacion...")
spooler = threading.Thread(target=Spooler, daemon=True)
spooler.start()
threads.append(spooler)

rawprint = threading.Thread(target=RawPrint, daemon=True)
rawprint.start()
threads.append(rawprint)

for index, thread in enumerate(threads):
    thread.join()

try:
    with open(PRINTNAME_PATH, "r") as FILE_RAW:
        PRINTERNAME = FILE_RAW.readline()
except FileNotFoundError:
    with open(PRINTNAME_PATH, "w") as FILE_RAW:
        FILE_RAW.write("Zebra ETC")
        FILE_RAW.close()
        PRINTERNAME = "Zebra ETC"


REQURL = f"{IP_RAW}:{PORT_RAW}"
PAYLOAD = json.dumps({
  "printer": PRINTERNAME,
  "data": "^XA^JUS^PW335^LL500^FWN^PR6^MD28^F050,50^BCN,100,Y,N,N^FD1234567890^FS^XZ"
})
RESPONSE = requests.request("POST", REQURL, data=PAYLOAD)

print(Fore.GREEN + "Calibracion enviada con exito.")
end = time.time()
print(f"Total time execution: {round(end-start,2)}")
