from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import re
import time
import pickle
import subprocess
from ipwhois import IPWhois
from os import system
import traceback

from modules.configuration import SQ_USER_NAME, SQ_PASSWORD, root_sidequest_url, all_apps_free_oculus_url, login_url, store_path
from modules.configuration import blue_color, red_color, green_color, yellow_color

from modules.headset_handler import get_installed_apks, get_installed_apks, get_apk_name, download_apk, get_installed_apks
from modules.sidequest_handler import get_sidequest_connections, detect_installation_process, monitor_installation, reboot_store

options = webdriver.ChromeOptions()
#options.add_argument("-headless")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)
cookie = None
session = None

prev_apks = None

def log_in():
    
    global cookie
    driver.get(login_url)
    email_field = driver.find_element(By.ID, 'login_email')
    email_field.send_keys(SQ_USER_NAME)
    time.sleep(1)
    pass_field = driver.find_element(By.ID, 'login_password')
    pass_field.send_keys(SQ_PASSWORD)
    time.sleep(1)
    button = driver.find_element(By.CLASS_NAME, 'aurora-button-square')
    button.click()
    time.sleep(1)
    
def crawl_apk(relative_path):
      
    prev_connections = get_sidequest_connections()
    app_url = root_sidequest_url + relative_path
    is_installed = False
    apk_name = None
    
    driver.get(app_url)
    time.sleep(1)
    name = driver.find_element(By.CLASS_NAME, 'mat-card-title').text
    error = None
    print(f'{blue_color}-----------Installing ' f'{green_color}{name}' + f'{blue_color}-----------')
    button = driver.find_element(By.CLASS_NAME, 'aurora-button-square')
    
    system('adb logcat -c') # Clear the logcat buffer
    time.sleep(1)
    if button.text == 'Sideload Now':
        button.click()
        time.sleep(2)

    
    elif button.text == 'Download Options':
        button.click()
        time.sleep(2)
        
        #-------------Select the device in the dropdown----------
        dropdown_item = driver.find_element(By.CLASS_NAME, 'mat-select-arrow')
        actions = ActionChains(driver)
        # Move to element and click
        actions.move_to_element(dropdown_item).click().perform()
        time.sleep(2)
        options = driver.find_elements(By.CLASS_NAME, 'mat-option-text')
        
        for option in options:
            if option.text == 'Meta Quest':
                actions = ActionChains(driver)
                actions.move_to_element(option).click().perform()
                time.sleep(2)
                break
        
        #-------------Click the Sideload Now button----------   
        buttons = driver.find_elements(By.CLASS_NAME, 'aurora-button-square')
        found_button = False
        for button in buttons:
            if button.text == 'Sideload Now':
                found_button = True
                button.click()
                time.sleep(2)
                break
        
        if not found_button:
            
            error = 'SIDEQUEST_BUTTON_NOT_FOUND'
            return False, name, None, error
    
    else:
        error = 'SIDEQUEST_BUTTON_NOT_FOUND'
        return False, name, None, error
    
    tries = 0
    is_installing = False
    while tries < 3 and is_installing == False:
        is_installing = detect_installation_process(prev_connections)
        if not is_installing: 
            print(f'{yellow_color}Retrying installation detection...')
            tries += 1
            time.sleep(1)
    
    if is_installing:
        is_installed, apk_name, error = monitor_installation(crawled_apks_name)
        
        if apk_name == None:
            post_apks = get_installed_apks()
            apk_name = get_apk_name(prev_apks, post_apks)
    else:
        error = 'CONNECTIONS_NOT_DETECTED'
        reboot_store()
          
    if is_installed or apk_name != None: return download_apk(apk_name), name, apk_name, error
    else: return False, name, None, error

def load_crawled_apks():

    try:
        crawled_apks = dict()
        crawled_apks_name = list()
        with open('crawled_apks.txt','r') as fd:
            lines = fd.read().strip().splitlines()
        
        for line in lines:
            parts = line.split('::')
            crawled_apks[parts[1]] = ({'app_name': parts[0], 'apk_dir':parts[1], 'apk_name': parts[2], 'status': parts[3]}) #The key is the directory of the app
            crawled_apks_name.append(parts[2])
            
        return crawled_apks, crawled_apks_name
    except Exception as e:
        return crawled_apks, crawled_apks_name

def store_crawled_apks():
    
    try:
                
        with open('crawled_apks.txt','w') as fd:
            for app in crawled_apks.values():
                fd.write(f'{app["app_name"]}::{app["apk_dir"]}::{app["apk_name"]}::{app["status"]}\n')
            
    except:
        with open('crawled_apks_dump.txt','wb') as fd:
            fd.write(pickle.dumps(crawled_apks))

def update_crawled_apks(app_name,app_dir,apk_name,status):
    
    global crawled_apks
    global crawled_apks_name
    
    if app_dir in crawled_apks:
        if apk_name != crawled_apks[app_dir]['apk_name']:
            
            crawled_apks_name.remove(crawled_apks[app_dir]['apk_name'])
            crawled_apks_name.append(apk_name)
                
            crawled_apks[app_dir]['apk_name'] = apk_name
            
        crawled_apks[app_dir]['status'] = status
    else:
        crawled_apks[app_dir] = {'app_name': app_name, 'apk_dir':app_dir, 'apk_name': apk_name, 'status': status}
        crawled_apks_name.append(apk_name)
    

prev_apks = get_installed_apks()
log_in()

driver.get(all_apps_free_oculus_url)
last_height = driver.execute_script("return document.body.scrollHeight")


exit_threshold = 0
apps_dirs_to_crawl = list()
while exit_threshold < 3:
    
    time.sleep(1)
    html = driver.page_source
    apps_dirs = re.findall(r'href=\"(\/app\/[^\"]+)',html)
    
    body = driver.find_element(By.TAG_NAME, "body")
    scroll_origin = ScrollOrigin.from_element(body)
    ActionChains(driver).scroll_from_origin(scroll_origin, 0, 3000).perform()
    
    if apps_dirs[0] not in apps_dirs_to_crawl:
        print('WARNING')
    new = 0
    for app_dir in apps_dirs:
        if app_dir not in apps_dirs_to_crawl:
            apps_dirs_to_crawl.append(app_dir)
            new += 1
    print(f'{blue_color} New apps: ' + f'{green_color}{new}' + f'{blue_color} Total apps: ' + f'{green_color}{len(apps_dirs_to_crawl)}')
    if new == 0:
        exit_threshold += 1

print(len(apps_dirs))

crawled_apks, crawled_apks_name = load_crawled_apks()

try:
    for app_dir in apps_dirs_to_crawl:
        
        if app_dir not in crawled_apks or crawled_apks[app_dir]['status'] != 'DOWNLOADED' and crawled_apks[app_dir]['status'] != 'SIDEQUEST_BUTTON_NOT_FOUND':
            is_crawled, app_name, apk_name, error = crawl_apk(app_dir)
            
            if is_crawled:
                print(f'\n{green_color}The app {app_name} has been crawled\n')
                update_crawled_apks(app_name,app_dir, apk_name,'DOWNLOADED')
            else:
                print(f'\n{red_color}The app {app_name} has not been crawled due to an error: {error}\n')
                update_crawled_apks(app_name,app_dir, None, error)
                
    store_crawled_apks()             
except KeyboardInterrupt:
    store_crawled_apks()
except Exception as e:
    print(f'Error---------------: {e} --> {traceback.print_exc()}')
    store_crawled_apks()

