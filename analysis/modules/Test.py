from modules.configuration import full_project_path
from modules.APK_Info import APK_Info
import subprocess

class Test():
    '''
    Test object save every variables and functions for the analysis
    Note that paths should be given relatively (e.g. )
    '''
    def __init__(self, script_name, args_list, binary_name):

        self.script_path = f'{full_project_path}scripts\\{script_name}'
        if type(args_list) is not list:
            raise TypeError
        self.args_list = args_list
        self.binary_name = binary_name
        
        self.command = None
        self.binary_path = None
    
    def generate_command(self):

        args_str = ''
        if self.args_list != None:
            for arg in self.args_list:
                args_str += f' {arg} '  

        self.command = ['powershell.exe','idat64', f'-A -S" {self.script_path}{args_str}" {self.binary_path}']

    def run(self, apk:APK_Info):
        
        if '.so' == self.binary_name[len(self.binary_name)-3:]:
            self.binary_path = f'{apk.decompiled_app_path}resources\\lib\\{apk.arch}\\{self.binary_name}'
        elif '.dll' == self.binary_name[len(self.binary_name)-4:]:
            self.binary_path = f'{apk.path_to_dlls}{self.binary_name}'
        self.generate_command()

        process = subprocess.Popen(self.command,stdin=subprocess.PIPE)
        process.wait()