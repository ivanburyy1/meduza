import pyautogui

def SetIpAddress():
    File_object = open(r"ipaddress", "w")
    ipaddress = None
    while(ipaddress == None):
        ipaddress = pyautogui.prompt("IP Медузы")
    File_object.write(ipaddress)
    File_object.close()
    return ipaddress

def GetIpAddress():
    try:
        File_object = open(r"ipaddress", "r")
        ip = File_object.read()
        File_object.close()
        return ip
    except FileNotFoundError:
        print("no ip address file")
        return SetIpAddress()
if __name__ == '__main__':
    print("Запустите Main.py")