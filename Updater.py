def Update():
    print("started updating")
    import wget
    import os
    import shutil
    filename = wget.download("https://github.com/ivanburyy1/meduza/archive/refs/heads/main.zip","")
    import zipfile
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall("")

    os.system(f"xcopy {os.path.dirname(os.path.realpath(__file__))}\meduza-main {os.path.dirname(os.path.realpath(__file__))} /E /H /C /I /Y")
    shutil.rmtree(f"{os.path.dirname(os.path.realpath(__file__))}\meduza-main")
    os.remove(f"{os.path.dirname(os.path.realpath(__file__))}\meduza-main.zip")
    print("finished")
def CheckForUpdate():
    import requests
    import os