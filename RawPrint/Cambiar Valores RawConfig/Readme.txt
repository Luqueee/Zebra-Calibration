Este codigo cambia el parametro de la IP de localhost a IP del HOST en RawPrint.exe.config alojado en la ruta: C:\Program Files (x86)\TreHoffman Technologies\RAW Print\RawPrint.exe.config

El proposito de este codigo es permitir hacer peticiones remotas a los ordenadores que tengan la Zebra conectada por USB.

Los requerimientos para hacer funcional el programa son los siguientes:
Este codigo para ser funcional necesita tener una regla de firewall la qual permita las peticiones via puerto 9100. 
Por otro lado se deberia hacer un tunnel desde la IP del host de la maquina al localhost:9100 o directamente permitir las peticiones directas a la IP del HOST via puerto 9100.
