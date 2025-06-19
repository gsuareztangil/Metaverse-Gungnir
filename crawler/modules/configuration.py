import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)  # Initialize colorama

blue_color  = Fore.BLUE
red_color = Fore.RED
green_color = Fore.GREEN
white_color = Fore.WHITE
yellow_color = Fore.YELLOW
reset_color = Style.RESET_ALL

SQ_USER_NAME = '' # This should be filled in
SQ_PASSWORD = '' # This should be filled in
root_sidequest_url = 'https://sidequestvr.com'
all_apps_free_oculus_url = 'https://sidequestvr.com/category/all?sortOn=downloads&app_license=FREE&app_platform=1&app_download_method=3'
login_url = 'https://sidequestvr.com/login'
store_path = '.\\Data\\APKs\\'