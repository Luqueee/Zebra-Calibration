import xml.dom.minidom as md 
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

PATH = "C:\Program Files (x86)\TreHoffman Technologies\RAW Print\RawPrint.exe.config"

file = md.parse(PATH)
print(file.nodeName)
print(file.firstChild.tagName)
adds = file.getElementsByTagName( "add" ) 

# printing the first name
print(file.getElementsByTagName("add")[0].setAttribute("value",f"http://{IPAddr}"))


with open(PATH, "w" ) as fs:  
  
        fs.write( file.toxml() ) 
        fs.close()  