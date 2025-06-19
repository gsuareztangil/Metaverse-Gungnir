
import re
import time
import subprocess
from ipwhois import IPWhois
from os import system
import traceback

from modules.configuration import blue_color, red_color, green_color, yellow_color
from modules.headset_handler import get_installed_apks, get_installed_apks, get_installed_apks

def get_sidequest_connections():
    
    conn_dict = dict()
    app_name = 'SideQuest.exe'
    
    try:
        # Run the command to detect the connections
        result = subprocess.run(f'powershell netstat -abnot', shell=True, check=True, capture_output=True, text=True)
        
        lines = result.stdout.strip().splitlines()
        connections = list()
        
        targeted_connections = False
        for line in lines: 
            if '[' in line and ']' in line:
                process_name = line.split('[')[1].split(']')[0]
                if process_name == app_name:
                    targeted_connections = True
                else:
                    targeted_connections = False
            elif 'Can not obtain ownership information' not in line and line != '' and line != 'Active Connections' and 'TCP' in line and 'UDP' not in line:
                if targeted_connections:
                    connections.append(line) 
        for connection in connections:
            parts = connection.split()
            #print(connection)
            
            conn_dict[f'{parts[1]}-{parts[2]}'] = {'protocol': parts[0], 'local_address': parts[1], 'foreign_address': parts[2], 'state': parts[3]}
        
        return conn_dict
    except subprocess.CalledProcessError as e:
        print(f'Error: {e} --> {e.output}')
    except Exception as e:
        for line in lines:
            print(line)

def detect_installation_process(prev): 
    
    post = get_sidequest_connections()
    cloudflare_connections = 0
    
    for connection in post.keys():
        
        local_address = post[connection]['local_address']
        foreign_adress = post[connection]['foreign_address']
        if local_address not in prev.keys() and '127.0.0.1' not in local_address and '0.0.0.0' not in foreign_adress:
            
            keep_trying = True
            seconds_to_wait = 1
            
            while keep_trying == True and seconds_to_wait < 10:
                try:
                    
                    address_to_check = foreign_adress.split(':')[0]
                    if address_to_check[-1] == '.': address_to_check = address_to_check[:-1]
                    whois_info = IPWhois(address_to_check).lookup_rdap()
                    keep_trying = False
                
                except ConnectionResetError as e:
                    time.sleep(seconds_to_wait)
                    seconds_to_wait += 1 
                except Exception as e:
                    time.sleep(seconds_to_wait)
                    seconds_to_wait += 1
            organization = ''
            if whois_info['asn_registry'] == 'ripencc':
                for object_key in whois_info['objects'].keys():
                    if 'ORG-' in object_key:
                        organization = whois_info['objects'][object_key]['contact']['name']
                        break
            else:
                organization = whois_info['objects'][list(whois_info['objects'].keys())[0]]['contact']['name']
            
            if organization == 'Cloudflare, Inc.':
                cloudflare_connections += 1
    
    if cloudflare_connections > 0:
        print(f'{blue_color} Detected ' + f'{green_color}{cloudflare_connections}' + f'{blue_color} connections to Cloudflare --> ' + f'{green_color}An installation process has been detected')
        return True
    else:
        print(f'{red_color}No connections to Cloudflare have been detected')
        return False

def reboot_store():
    
    store_name = 'SideQuest'
    path_store = 'C:\\Program Files\\SideQuest\\SideQuest.exe'
    try:
        system(f'powershell -Command "Stop-Process -Name {store_name} -Force -ErrorAction SilentlyContinue"')
        
        # Define the PowerShell command to run
        command = f'Start-Process "{path_store}"'

        # Use subprocess to run the PowerShell command
        result = subprocess.run(["powershell", "-Command", command], shell=True, check=True, capture_output=True, text=True)
        time.sleep(5)
    except Exception as ex:
        print(f'Error: {ex} --> {traceback.print_exc()}')
        
def monitor_installation(crawled_apks_name:list = None):
    
    time_limit = 3 * 60
    
    #system('adb logcat -c') # Clear the logcat buffer
    # Start the logcat command using subprocess
    process = subprocess.Popen(
        ['adb', 'logcat'],  # Command to execute
        stdout=subprocess.PIPE,  # Capture the output (stdout)
        stderr=subprocess.PIPE,  # Capture error output (stderr)
        text=True,              # This ensures the output is treated as text (str)
        encoding='utf-8',       # Forces the process output to be decoded as UTF-8
        errors='replace'        # Replace any invalid characters with a placeholder
    )

    # Continuously read the output of logcatz
    try:
        download_detected = False
        package_installation_has_begun = False
        package_installation_has_ended = False
        is_installed = False
        apk_name = None
        installation_process_init_timestamp = time.time()
        
        while True:
            output = process.stdout.readline()  # Read each line from logcat output
            if output == '' and process.poll() is not None:
                break
            if output:
              
                
                if 'installd' in output and '--- BEGIN' in output:
                    
                    apk_name_output = output[output.find("'")+1:].split('/')[4].split('-')[0] # Extract APK name from the log
                    if apk_name == None and apk_name not in crawled_apks_name: 
                        apk_name = apk_name_output
                    
                    if apk_name == apk_name_output: 
                        package_installation_has_begun = True
                        package_installation_has_ended = False
                        print('Package installation process starting...')
                    
                elif 'installd' in output and '--- END' in output:
                    
                    some_apk_name = output[output.find("'")+1:].split('/')[4].split('-')[0] # Extract APK name from the log
                    
                    if some_apk_name not in crawled_apks_name:
                        apk_name_output = some_apk_name
                    
                    if apk_name == apk_name_output:
                        package_installation_has_begun = False
                        package_installation_has_ended = True
                        reference_timestamp = time.time()
                        print('Package installation process finished')
                
                elif 'MediaProvider' in output and 'android.intent.action.PACKAGE_ADDED' in output and apk_name == None:
                    is_installed = True
                    some_apk_name = re.findall('(?:[a-zA-Z0-9_-]*[a-zA-Z_-]+[a-zA-Z0-9_-]*\.)+[a-zA-Z0-9_-]*[a-zA-Z_-]+[a-zA-Z0-9_-]*',output)[0]
                    
                    if some_apk_name not in crawled_apks_name:
                        apk_name = some_apk_name
                    if 'Invalidating LocalCallingIdentity cache' in output:
                        print(f'{yellow_color}Installation detected for {apk_name}')
                        is_installed = True
                        break
                    
                if package_installation_has_ended:
                    elapsed_time = time.time() - reference_timestamp
                    if elapsed_time > 10:
                        is_installed = True
                        break
                
                if 'PackageInstaller' in output and 'INSTALLATION_FAILED' in output:
                    print('The installation has failed.')
                    return is_installed, None, 'INSTALLATION_FAILED'
                
                if is_installed:
                    if apk_name == None and 'BackupManagerService' in output and 'restoreAtInstall' in output:
                        apk_name = output[output.find('pkg=')+4:output.find('token=')].strip() # Extract APK name from the log
                        print(f'The apk {apk_name} has been installed')
                    
                    if apk_name != None:
                        installed = get_installed_apks()
                        if apk_name in installed:
                            print(f'{apk_name} is is detected in the device')
                            process.terminate()
                            break
            if time.time() - installation_process_init_timestamp > time_limit:
                    print('The installation process has taken too long and will be considered as failed')
                    reboot_store()
                    break
        return is_installed, apk_name, None
                        
                

    except KeyboardInterrupt:
        # Stop the subprocess when you stop the script
        process.terminate()

    process.wait()