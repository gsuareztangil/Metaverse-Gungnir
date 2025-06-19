import subprocess
from os import system

from modules.configuration import store_path
from modules.configuration import blue_color, red_color, green_color

def get_installed_apks():
    try:
        result = subprocess.run('adb shell pm list packages', shell=True, check=True, capture_output=True, text=True)
        
        packages = result.stdout.strip().replace('package:','').split('\n')
        #print(packages)
        return packages
    except subprocess.CalledProcessError as e:
        return f"{e} --> {e.stderr.strip()}"

def get_apk_name(prev:list,post:list):
    
    for package in post:
        if package not in prev:
            print(f'{blue_color}The apk name is: ' + f'{green_color}{package}')
            return package
    
    return None
def get_count_downloaded_apks():
    
    downloaded_apks = list()
    result = subprocess.run(f'powershell -Command "(dir {store_path}  | Select-Object -Property Name).Count"', shell=True, check=True, capture_output=True, text=True)
    raw_exit = result.stdout.strip().splitlines()[1:]
    
    for line in raw_exit:
        downloaded_apks.append(line.split(' ')[-1])
    
    return downloaded_apks

def get_downloaded_apks():
    
    downloaded_apks = list()
    result = subprocess.run(f'powershell -Command "dir {store_path}  | Select-Object -Property Name"', shell=True, check=True, capture_output=True, text=True)
    raw_exit = result.stdout.strip().splitlines()[2:]
    
    for line in raw_exit:
        downloaded_apks.append(line.strip())
    
    return downloaded_apks
 
def download_apk(apk_name): 
    
    is_downloaded = False
    try:
        print(f'{blue_color}-----------Finding the path of APK-----------')
        path = subprocess.run('adb shell pm path ' + apk_name, shell=True, check=True, capture_output=True, text=True).stdout.strip().replace('package:','')
        print(f'{green_color}{path}')

        print(f'{blue_color}-----------Downloading APK-----------')
        downloaded_apks = get_downloaded_apks()
        previous_apk_count = len(downloaded_apks)
        result = subprocess.run('adb pull ' + path + ' ' + store_path, shell=True, check=True, capture_output=True, text=True)
        
        print(f'{blue_color}-----------Modifying APK package name-----------')
        result = subprocess.run(f'powershell -Command "ren {store_path}base.apk {apk_name}.apk"', shell=True, check=True, capture_output=True, text=True)
        result = subprocess.run(f'powershell -Command "dir {store_path}  | Select-Object -Property Name | findstr {apk_name}"', shell=True, check=True, capture_output=True, text=True)
        if apk_name in result.stdout.strip():
            print(f'{blue_color}Name modified: ' + f'{green_color}{result.stdout.strip()}')
        downloaded_apks = get_downloaded_apks()
        post_apk_count = len(downloaded_apks)
        if previous_apk_count == post_apk_count and apk_name+'.apk' not in downloaded_apks:
            print(f'{green_color}[WARNING]: The APK could not be downloaded')
            return False
        else:
            is_downloaded = True
        print(f'{blue_color}-----------Deleting APK-----------')
        result = subprocess.run('adb shell pm uninstall ' + apk_name, shell=True, check=True, capture_output=True, text=True)
        print(f'{green_color}{result.stdout.strip()}')
        
        return is_downloaded
    except subprocess.CalledProcessError as e:
        print(f'{red_color}{e} --> {e.stderr.strip()}')
        if 'ren : Cannot create a file when that file already exists.' in e.stderr: 
            system(f'powershell -Command "del {store_path}base.apk"')
            uninstall_app(apk_name)
            
            return True
        return is_downloaded

def get_installed_apks():
    try:
        result = subprocess.run('adb shell pm list packages', shell=True, check=True, capture_output=True, text=True)
        
        packages = result.stdout.strip().replace('package:','').split('\n')
        return packages
    except subprocess.CalledProcessError as e:
        return f"{e} --> {e.stderr.strip()}"

def uninstall_app(apk_name):
    try:
        print('-----------Deleting APK-----------')
        result = subprocess.run('adb shell pm uninstall ' + apk_name, shell=True, check=True, capture_output=True, text=True)
        print(f'{green_color}{result.stdout.strip()}')
        return True
    except subprocess.CalledProcessError as e:
        return False