import os
from colorama import just_fix_windows_console, init, Fore, Back, Style
import json

init(autoreset=True)

MENU_PRINCIPAL = '''
1.Crear una nueva relacion IP-HOST
2.Modificar una relacion IP-HOST
3.Eliminar una relacion IP-HOST
          '''
          
MENU_ELIMINAR = '''
1.Eliminar por IP
2.Eliminar por HOST
'''

def menuRelacion(PALABRA_MENU):
    print(f'''
1.{PALABRA_MENU} IP buscando por HOST
2.{PALABRA_MENU} IP buscando por IP
3.{PALABRA_MENU} HOST buscando por IP
4.{PALABRA_MENU} HOST buscando por HOST

''')



PATH_JSON = 'IPsZebras.json' 


def menuEliminar():
    while True:
        print(MENU_ELIMINAR)
        OP = input('Ingrese una opcion: ')
        if OP in ["1","2"]:
            return int(OP)
        else:
            CleanScreen()
            wrongOption()

def readJSON():
    with open(PATH_JSON, 'r') as f:
        data = json.load(f)
    return data

def dumpJSON(data):
    with open(PATH_JSON, 'w') as f:
        json.dump(data, f, indent=4)

def wrongOption():
    print(Fore.RED + 'Opcion incorrecta')
    print('')

def getIP():
    while True:
        IP = input("Ingrese la IP: ")
        if len(IP.split('.')) == 4 and len(IP) > 4 and "N" not in IP:
            return IP
        else:
            print(Fore.RED + 'La IP no es valida')
            print('')
  

def getHOST():
    while True:
        HOST = input("Ingrese el HOST: ")
        if len(HOST) > 0 and "N" in HOST:
            return HOST
        else:
            print(Fore.RED + 'El HOST no puede estar vacio y no puede contener la letra N')
            print('')

def CleanScreen():
    os.system('cls')
 

def MenuModify():
    while True:
        
        menuRelacion('Modificar')
        OP = input('Ingrese la opcion(1-4): ')
        if OP in ["1","2","3","4"]:
            return int(OP)
        else:
            CleanScreen()
        wrongOption()

def FindValuesInData(IP = "", HOST = ""):
    data = readJSON()
    for IP_, HOST_ in data['RELACION_IP_HOST'].items():
        if IP == IP_ and HOST == HOST_:
            return -1, IP, HOST
        if IP == IP_:
            return 0, IP, HOST_
        if HOST == HOST_:
            return 1,IP_, HOST
        
    return 2, None, None


 


def menuIP():
    while True:
        print(MENU_PRINCIPAL)
        OP = input('Ingrese una opcion: ')
        
        if OP in ["1","2","3","4"]:
            return int(OP)
        else:
            CleanScreen()
            wrongOption()

data = readJSON()

while True:
    op = menuIP()

    if op == 1:
        IP = getIP()
        HOST = getHOST()
        TYPE_RELATION, IP_SEARCH, HOST_SEARCH = FindValuesInData(IP, HOST)
        print(TYPE_RELATION, IP_SEARCH, HOST_SEARCH)
        
        #-1 == RELACION EXISTENTE
        #0 == IP EXISTENTE
        #1 == HOST EXISTENTE
        #2 == NO EXISTE RELACION
        
        if TYPE_RELATION == -1:
            print(Fore.RED + f'La relacion {IP}-{HOST} ya existe')
            exit()
        elif TYPE_RELATION == 0:
            print(Fore.RED + f'La IP {IP} ya esta asignada al host {HOST_SEARCH}')
            exit()
        elif TYPE_RELATION == 1:
            print(Fore.RED + f'El HOST {HOST} ya esta asignado a otra {IP_SEARCH}')
            exit()
        elif TYPE_RELATION == 2:
            data['RELACION_IP_HOST'][IP] = HOST
            dumpJSON(data)
            print("Relacion IP-HOST creada con exito")
            
    if op == 2:
        OP_MODIFY = MenuModify()    
        
        if OP_MODIFY == 1:
            #Modificar IP buscando por HOST
            print("MENU: Modificar IP buscando por HOST")
            
            HOST = getHOST()
            TYPE_RELATION, IP_SEARCH, HOST_SEARCH = FindValuesInData(HOST=HOST)
            print(TYPE_RELATION, IP_SEARCH, HOST_SEARCH)
            
            if TYPE_RELATION == 1:
                NEW_IP = getIP()
                data["RELACION_IP_HOST"][NEW_IP] = data["RELACION_IP_HOST"].pop(IP_SEARCH)
                dumpJSON(data)
            #-1 == RELACION EXISTENTE
            #0 == IP EXISTENTE
            #1 == HOST EXISTENTE
            #2 == NO EXISTE RELACION
        
        if OP_MODIFY == 2:
            #Modificar IP buscando por IP
            print("MENU: Modificar IP buscando por IP")
            IP = getIP()
            TYPE_RELATION, IP_SEARCH, HOST_SEARCH = FindValuesInData(IP=IP)
            print(TYPE_RELATION, IP_SEARCH, HOST_SEARCH)
            
            if TYPE_RELATION == 0:
                NEW_IP = getIP()
                data["RELACION_IP_HOST"][NEW_IP] = data["RELACION_IP_HOST"].pop(IP)
                dumpJSON(data)
            else:
                print(Fore.RED + f'La IP {IP} no existe')
                exit()
        
        if OP_MODIFY == 3:
            #Modificar HOST buscando por IP
            print("MENU: Modificar HOST buscando por IP")
            IP = getIP()
            TYPE_RELATION, IP_SEARCH, HOST_SEARCH = FindValuesInData(IP=IP)
            print(TYPE_RELATION, IP_SEARCH, HOST_SEARCH)
            
            if TYPE_RELATION == 0:
                NEW_HOST = getHOST()
                data["RELACION_IP_HOST"][IP] = NEW_HOST
                dumpJSON(data)
            else:
                print(Fore.RED + f'La IP {IP} no existe')
                exit()
        if OP_MODIFY == 4:
            #Modificar HOST buscando por HOST
            print("MENU: Modificar HOST buscando por HOST")
            HOST = getHOST()
            TYPE_RELATION, IP_SEARCH, HOST_SEARCH = FindValuesInData(HOST=HOST)
            print(TYPE_RELATION, IP_SEARCH, HOST_SEARCH)
            
            if TYPE_RELATION == 1:
                NEW_HOST = getHOST()
                TYPE_RELATION_NEW_HOST, IP_RELATION_HOST, _ = FindValuesInData(HOST=HOST)

                if TYPE_RELATION_NEW_HOST == 2:
                    
                    data['RELACION_IP_HOST'][IP_RELATION_HOST] = NEW_HOST
                    dumpJSON(data)
                if TYPE_RELATION_NEW_HOST == 1:
                    _, IP_RELATION_NEW_HOST, _ = FindValuesInData(HOST=NEW_HOST)

                    print(Fore.RED + f'El HOST {NEW_HOST} ya esta asignada a la IP {IP_RELATION_NEW_HOST}')
                    exit()
            else:
                print(Fore.RED + f'El HOST {HOST} no existe')
                exit()
    
    if op == 3:
        print("Eliminar relacion IP-HOST")
        OP = menuEliminar()
        # 1 POR IP
        # 2 POR HOST
        
        if OP == 1:
            IP = getIP()
            TYPE_RELATION, IP_SEARCH, HOST_SEARCH = FindValuesInData(IP=IP)
            print(TYPE_RELATION, IP_SEARCH, HOST_SEARCH)
            if TYPE_RELATION == 2:
                print(Fore.RED + f'La relacion IP-HOST no existe')
                exit()
            else:
                data['RELACION_IP_HOST'].pop(IP_SEARCH)
                dumpJSON(data)
                print("Relacion IP-HOST eliminada con exito")
        if OP == 2:
            HOST = getHOST()
            TYPE_RELATION, IP_SEARCH, HOST_SEARCH = FindValuesInData(HOST=HOST)
            print(TYPE_RELATION, IP_SEARCH, HOST_SEARCH)
            if TYPE_RELATION == 2:
                print(Fore.RED + f'La relacion IP-HOST no existe')
                exit()
            else:
                data['RELACION_IP_HOST'].pop(IP_SEARCH)
                dumpJSON(data)
                print("Relacion IP-HOST eliminada con exito")