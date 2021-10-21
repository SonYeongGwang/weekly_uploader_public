import dropbox
import os
import time
import datetime
from datetime import timedelta

#=====================Personal Information======================
# NAS log-in id and password
NAS_USER_NAME = ''
NAS_PASSWORD = ''
# DropBox token to access DropBox folder
# Create DropBox token here: https://www.dropbox.com/developers
access_token = ''
#===============================================================

month = time.strftime('%m', time.localtime(time.time()))
today = datetime.datetime.today()
days_passed_from_monday = today.weekday()
delta = today - timedelta(days=days_passed_from_monday)

target_folder = delta.strftime("%Y%m%d")+"_Weekly_Report"
print("<<Weekly Uploader>>")
print(" ")
print("INFO: System will download files from ----> " + target_folder)

# ask to the user whether proceed or not
while True:
    response = input("Continue to Download? (Y/N): ")
    if response=='Y' or response=='y':
        print(response)
        break
    elif response=='N' or response=='n':
        print("Program will be closed")
        input("Press enter to exit...")
        exit()
    else:
        print("Warning: Wrong input command! Enter proper command.")
        input("Press enter and retry...")
        continue

# Target Paths for DropBox and NAS
target_path = '/IRMS Lab Folder/'+ target_folder
nas_target_path = 'Z:\\12.연구실_주간미팅'

# Check whether target folder already exists in NAS
# Access to NAS first,
print("INFO: Accessing to NAS...")
os.system(r"NET USE Z: \\robottory.synology.me\Robottory_Data " + NAS_PASSWORD + " " + "/user:" + NAS_USER_NAME)
print("Please Note: (시스템 오류 85 doesn't mean that it is not going to be worked)")
print("INFO: Successfully accessed to NAS!")
print("INFO: Checking for existence of target folder in the NAS directory...")
existence = os.path.isdir(nas_target_path + '\\' + target_folder)

# Exit when the target folder already exists in NAS
if existence == True:
    print("INFO: " + target_folder + " is already exist!")
    input("Press enter to exit...")
    exit()
elif existence == False:
    print("INFO: Download will be started...")

else:
    print("Existence Checking Error!")
    input("Press enter to exit...")

with dropbox.Dropbox(access_token) as dbx:
    try:
        dbx.users_get_current_account()
        print("INFO: Successfully got the user account")
    except:
        print("ERROR: Invalid access token; try re-generating an "
                 "access token from the app console on the web.")
        input("Press enter to exit...")
        exit()

    if os.path.isdir('./temp'):
        os.system("rmdir /s /q" + " " + ".\\" + 'temp\\')
    os.mkdir('./temp')
    with open('./temp/' + target_folder+'.zip', 'wb') as f:
        # download zip files from dropbox
        print("INFO: Downloading files..." + target_folder)
        metadata, res = dbx.files_download_zip(path=target_path)
        f.write(res.content)
        print("INFO: Successfully Downloaded")

print("INFO: Unzip using Bandizip...")
os.system("Bandizip.exe x -o:.\\" + 'temp\\' + " " + ".\\" + 'temp\\' +target_folder + ".zip")
os.system(r"del" + " " + ".\\" + 'temp\\' + target_folder + ".zip")
print("INFO: Moving folder to NAS directory...")
os.system("mkdir" + " " + nas_target_path + "\\" + target_folder)
os.system("xcopy .\\" + 'temp\\' + target_folder + "\\*.*" + " " + nas_target_path + "\\" + target_folder + " " + "/e /h /k")
os.system("rmdir /s /q" + " " + ".\\" + 'temp\\' + target_folder)
os.system("rmdir /s /q" + " " + ".\\" + 'temp\\')
print("INFO: All weekly files are moved to NAS successfully")
os.system("start Z:\\12.연구실_주간미팅")
input("Press enter to exit...")
exit()
