import multiprocessing
def Request(ipaddress):
    #import all of the modules and set all the variables
    import requests
    import os
    import pandas
    from datetime import datetime
    exampledf = pandas.DataFrame(columns=["Время","Температура","Кислотность","Соль","Кислород"],dtype=str)
    # -
    # get all of the information from esp
    temp = requests.post(f"http://{ipaddress}/temp/").text
    acid = requests.post(f"http://{ipaddress}/ph/").text
    salt = requests.post(f"http://{ipaddress}/salt/").text
    oxygen = requests.post(f"http://{ipaddress}/oxygen/").text
    # -
    #check if file exist and create if doesnt
    tryagainstep = 0
    while(tryagainstep != 5):
        try:
            exists = os.path.exists(os.path.dirname(os.path.realpath(__file__)) + "\\" + "ExcelFiles" + "\\" + datetime.now().strftime("%B %d, %Y") + ".xlsx")
            print(exists)
            if not exists:
                exampledf.to_excel("ExcelFiles" + "\\"+ datetime.now().strftime("%B %d, %Y") + ".xlsx", engine='xlsxwriter')
                print("created file")
            break
        except:
            print("File possibly open did not check the existence of file, permission denied,retrying")
            tryagainstep += 1
            if(tryagainstep == 5):
                raise TimeoutError("Cant check file, timeouted 5 checks")
                  
    # -
    #read excel file to continue making it
    df = pandas.read_excel("ExcelFiles" + "\\" + datetime.now().strftime("%B %d, %Y") + ".xlsx",index_col=0,sheet_name=0, header=0, names=None, usecols=None)
    # -
    #return the value and save it into excel file
    dfpreset = pandas.DataFrame([(datetime.now().strftime("%H:%M"),temp,acid,salt,oxygen)],columns=["Время","Температура","Кислотность","Соль","Кислород"],dtype=str)
    dfconcat = pandas.concat([df,dfpreset])
    tryagainstep = 0
    while(tryagainstep != 5):
        try:                    
            dfconcat.to_excel("ExcelFiles" + "\\" + datetime.now().strftime("%B %d, %Y") + ".xlsx", engine='xlsxwriter')
            break
        except:
            print("file open can not save data,trying again")
            if(tryagainstep == 5):
                print("file save timeout did not save.")
                break
            tryagainstep += 1
    return temp,acid,salt,oxygen
    # -

if __name__ == '__main__':
    multiprocessing.freeze_support()
    print("Запустите Main.py")