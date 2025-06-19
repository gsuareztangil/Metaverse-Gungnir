import os
import subprocess
import traceback
import re
from modules.configuration import *
from modules.APK_Info import APK_Info
from modules.Test import Test

def parse_to_hex(byte_sequence):
    
    return ":".join(format(byte, '02X') for byte in byte_sequence)

def decompile_app(apk:APK_Info):
    '''
    It decompiles an APK using Jadx.
    '''
    
    apk_folder = apk.apk_name.replace('.','_')
    apkdir = f'.\\Data\\{apk_folder}\\'
    decompiled_folder = f'decompiled_{apk_folder}'
    decompiled_app_path = f'{full_project_path}{apkdir[2:]}{decompiled_folder}\\'
    apk.decompiled_app_path = decompiled_app_path
    dirs = os.listdir(apkdir)
    
    if(decompiled_folder not in os.listdir(apkdir)):
        print(f'Decompiling {apk.apk_name}')
        try:
            print(('Decompiling ') + (apk.apk_name) + (' (...)'))
            result = subprocess.run('jadx -d  ' + decompiled_app_path + ' ' + apk.apk_path + apk.apk_file_name, shell=True, check=True, capture_output=True, text=True)
            result = result.stdout.strip()
            print(('The decompilation of ') + (apk.apk_name) + (' has been finished'))
        except Exception as e:
            print('[ERROR]: ' + str(e))

    apk.arch = get_arch(apk)  
    return decompiled_app_path
    
def remove_app(decompiled_app_path):
    
    apk_name = decompiled_app_path[decompiled_app_path.find("_"):]
    try:
        
        print(('Removing ') + (apk_name) + (' (...)'))
        result = subprocess.run('rm -r  ' + decompiled_app_path, shell=True, check=True, capture_output=True, text=True)
        print(('The app ') + (apk_name) + (' has been removed'))
        
       
    except Exception as e:
        print('[ERROR]: ' + str(e))

def get_arch(apk:APK_Info):
    
    try:
        result = subprocess.run('dir /b ' +  apk.decompiled_app_path + path_binaries, shell=True, check=True, capture_output=True, text=True)
        archs = result.stdout.strip().splitlines()
        return archs[0]
    except:
        return 'None'

def get_dll_sdks(apk:APK_Info):

    dll_sdks_list = list()
    dll_class_list = list()
    try:

        result = subprocess.run(f'wsl ls {transfor_to_wsl_path(data_path + apk.apk_name)}/results/dll_classes', shell=True, check=True, capture_output=True, text=True)
        dlls = result.stdout.strip().splitlines()
        
        for dll in dlls:
            dll_name = dll.replace('.txt','')
            with open(f'{data_path}{apk.apk_name}\\results\\dll_classes\\{dll}', 'r') as fd:
                classes = fd.readlines()
            
            for class_name in classes:
                if class_name not in dll_class_list and dll_name in class_name:
                    dll_class_list.append(class_name.strip())
        
        dll_sdks_list = list()
        while (len(dll_class_list) > 0):
            reference_lib = dll_class_list.pop(0)
            if '`' in reference_lib: reference_lib = reference_lib[:reference_lib.find('`')]
            parts = reference_lib.split('.')
            if len(parts) == 1: continue
            reference = parts[0]
            
            local_list = list()
            is_sdk = False
            sdk = ''
            while(is_sdk == False):
                
                if local_list != []:
                    
                    is_in_all = True
                    for local_lib in local_list:
                        if reference not in local_lib[:len(reference)]:
                            is_in_all = False
                            break
                    if not is_in_all:  
                        possible_sdk = reference[:len(reference)-1]
                        if '.' in possible_sdk: 
                            if possible_sdk.count('.') > 1: sdk= '.'.join(reference.split('.')[:len(reference.split('.'))-1])
                            else: sdk= '.'.join(reference.split('.')[:len(reference.split('.'))]) 
                        else: break
                        is_sdk = True
                    else:
                        if (len(parts) == len(reference.split('.'))):
                            possible_sdk = reference[:len(reference)-1]
                            if '.' in possible_sdk:
                                if possible_sdk.count('.') > 1: sdk= '.'.join(reference.split('.')[:len(reference.split('.'))-1])
                                else: sdk= '.'.join(reference.split('.')[:len(reference.split('.'))])
                            else: break
                            is_sdk = True
                        else:
                            reference = '.'.join(parts[:len(reference.split('.'))+1])
                else:
                    for lib in dll_class_list.copy():#Populate with the lines with similar parts
                        if reference in lib[:len(reference)]:
                            local_list.append(lib)
                    if local_list == []: #It not it can be the only one. It checks the size of other similars with the same parts since the last always remain in the first item
                        n_parts_in_sdk_list = list()
                        lenght_of_similars = list()
                        for sdk in dll_sdks_list:#It checks the depth in the mane of sdks that are owned by the same owner
                            n_parts_in_sdk = 0
                            lenght_of_similar = 0
                            for counter, part in enumerate(parts):
                                local_sdk = '.'.join(parts[:counter+1])
                                if len(sdk) >= len(local_sdk) and part in sdk[:len(local_sdk)]:
                                    n_parts_in_sdk += 1
                                    if lenght_of_similar == 0: lenght_of_similar = len(sdk.split('.'))
                                else: break
                            
                            if n_parts_in_sdk > 0: n_parts_in_sdk_list.append(n_parts_in_sdk)
                            if lenght_of_similar > 0: lenght_of_similars.append(lenght_of_similar)
                            
                        if n_parts_in_sdk_list != [] and max(n_parts_in_sdk_list) > 0:
                            
                            sdk = '.'.join(parts[:min(max(max(n_parts_in_sdk_list),max(lenght_of_similars)),len(parts))])
                            is_sdk = True
                            break

                    if local_list == []:
                        sdk = '.'.join(reference.split('.')[:len(reference.split('.'))])
                        if sdk == '' or '.' not in sdk: 
                            len_parts = len(parts)
                            sdk = '.'.join(parts[:1 if len_parts == 1 else 2 if len_parts > 1 else 1]) #the last 1 is only to close the sentence
                        is_sdk = True
            
            if is_sdk == True:
                for lib in dll_class_list.copy():
                    if sdk in lib[:len(reference)]:
                        dll_class_list.remove(lib)
                
                if sdk not in dll_sdks_list: dll_sdks_list.append(sdk)
        
        with open('.\\graphs\\freq\\\dll_sdks.csv', 'a') as fd:    
            for sdk in dll_sdks_list:
                fd.write(f'{sdk},{apk.apk_name}\n')
        with open('.\\graphs\\freq\\dll_sdks_reverse.csv', 'a') as fd:    
            for sdk in dll_sdks_list:
                fd.write(f'{apk.apk_name},{sdk}\n')  
              
        return dll_sdks_list

    except Exception as e:
        print('[ERROR]: ' + str(e))
        stack_trace = traceback.format_exc()
        print(stack_trace)
    
def get_android_sdks(apk:APK_Info):
    
    global third_libraries
    global total_unity_libs
    global total_native_libs
    global total_unreal_libs
    global analytics

    third_libraries = list()
    result_lines = list()
    apk_path = apk.apk_path
    
    sources_path = transfor_to_wsl_path(apk.decompiled_app_path + path_sources)
    try:
        print('Extracting third party libraries of ' + apk_path + apk.apk_name + ' (...)')
        result = subprocess.run('wsl find ' + sources_path, shell=True, check=True, capture_output=True, text=True)
        result = result.stdout.strip()
        result = result.replace('.DS_Store','')
        result = result.replace('//','/')
        aa = f'{transfor_to_wsl_path(apk.decompiled_app_path)[:]}sources/'
        result = result.replace(f'{transfor_to_wsl_path(apk.decompiled_app_path)[:]}sources/','').strip()
        
        lines = result.splitlines()
        
        for line in lines:
            line = line.replace('./','')
            line = line.replace('//','/')
            
            if line[len(line)-5:] != '.java': result_lines.append(line) 
        print('Third party libraries extracted.')
        
        package_name = apk.apk_name.replace('.apk','')
        package_name = package_name.replace('com_','')
        
        forbidden_domains = package_name.split('.') 
        for domain in forbidden_domains:
            for line in result_lines.copy():
                if domain in line: result_lines.remove(line)
        
        counter = 0 
        while (len(result_lines) > 0):
            
            minimization_list = [result_lines.pop(0)]
            
            while (len(minimization_list) > 0):
                new_match = False
                reference = minimization_list.pop(0)
                
                        
                reference_parts = reference.split('/')
                reference_level = len(reference_parts)
                for cursor in result_lines:
                    
                    cursor_parts = cursor.split('/')
                    cursor_level = len(cursor_parts)

                    if reference in cursor[:len(reference)] and cursor_level > reference_level:
                        minimization_list.append(cursor)
                        result_lines.remove(cursor)
                        new_match = True
                if new_match == False: 
                    third_libraries.append(reference)
                    
            counter += 1

        sdk_list = list()
        apk_name_parts = apk.apk_name.split('_')
        while (len(third_libraries) > 0):
            reference_lib = third_libraries.pop(0)
            parts = reference_lib.split('/')
            if apk_name_parts[0] in parts[0]:
                if apk_name_parts[1] in parts[1]:
                    continue

            reference = ''
            
            is_min_reference = False
            part_counter = 0
            while (is_min_reference == False):
                
                if part_counter < len(parts): 
                    reference = '/'.join(parts[:part_counter+1])
                else: break
                
                if reference not in tlds and reference not in owners and parts[part_counter] not in owners: 
                    is_min_reference = True
                part_counter += 1   
            
            local_list = list()
            is_sdk = False
            sdk = ''
            while(is_sdk == False):
                
                if local_list != []:  
                    is_in_all = True
                    for local_lib in local_list:
                        if reference not in local_lib:
                            is_in_all = False
                            break
                    if not is_in_all:
                        
                        possible_sdk = reference[:len(reference)-1]
                        if possible_sdk not in tlds and possible_sdk not in owners: sdk = '/'.join(reference.split('/')[:len(reference.split('/'))-1]) 
                        else: sdk = reference
                        if sdk == '': 
                            sdk = reference
                        is_sdk = True
                    else:
                        if (len(parts) == len(reference.split('/'))):
                            possible_sdk = reference[:len(reference)-1]
                            if possible_sdk not in tlds and possible_sdk not in owners: sdk = '/'.join(reference.split('/')[:len(reference.split('/'))-1])
                            else: sdk = reference
                            if sdk == '': 
                                sdk = reference
                            is_sdk = True
                        else:
                            reference = '/'.join(parts[:len(reference.split('/'))+1])
                else:
                    for lib in third_libraries.copy():
                        if reference in lib:
                            local_list.append(lib)
                    if local_list == []:
                        
                        sdk = '/'.join(reference.split('/')[:len(reference.split('/'))])
                        if sdk == '' or '/' not in sdk: 
                            len_parts = len(parts)
                            sdk = '/'.join(parts[:1 if len_parts == 1 else 2 if len_parts > 1 else 1]) #the last 1 is only to close the sentence
                        is_sdk = True
            
            for lib in third_libraries.copy():
                if sdk in lib[:len(sdk)]:
                    third_libraries.remove(lib)
            sdk_list.append(sdk.replace('/','.'))
  
        return sdk_list
    except Exception as e:
        print('[ERROR]: ' + str(e))



def check_unity_version(apk:APK_Info):
    '''
    It checks in the hexadecimal of libunity.so for the Unity Version
    '''
    
    app_libunity_path = apk.decompiled_app_path + libunity_path
    
    try:

        app_libunity_path =  apk.decompiled_app_path + libunity_path.replace('++--++', apk.arch)
        
        if os.path.exists(app_libunity_path):

            print(('Checking Unity Version of ') + ( apk.apk_name) + (' (...)'))
            result = subprocess.run('readelf -n ' + app_libunity_path, shell=True, check=True, capture_output=True, text=True)
            notes = result.stdout.strip()
            if '.note.unity' in notes:
                unity_note = notes[notes.find('.note.unity'):].splitlines()
                unity_version = unity_note[3].replace('description data:','').replace(' ','')
                            
                unity_version = bytes.fromhex(unity_version).decode('utf-8').split('_')[0]
                apk.apk_unity_version = unity_version
            else:
                assets_path = apk.decompiled_app_path + '\\resources\\assets\\bin\\Data\\'
                unix_assets_path = transfor_to_wsl_path(assets_path)
                if os.path.exists(assets_path):
                    assets = os.listdir(assets_path)
                    
                    for asset in assets:
                        result = subprocess.run(f'wsl xxd -s 0x14 -l 16 {unix_assets_path}{asset} ', shell=True, check=True, capture_output=True, text=True)
                        notes = result.stdout.strip()
                        version = re.findall(r'(\d{4}\.\d+\.\d+[fbp]\d+|\d\.\d+\.\d+[fbp]\d+)', notes)
                        if version != []:
                            unity_version = version[0]
                            apk.apk_unity_version = unity_version
                            break

            return True, unity_version
        else: 
            return False, None

    except Exception as e:
        print('[ERROR]: ' + str(e))

def check_unreal(apk:APK_Info):
    
    try:
        
        app_libUE4_path = apk.decompiled_app_path + libUE4_path.replace('++--++', apk.arch)
        
        if os.path.exists(app_libUE4_path):
            return True
        else: 
            return False

    except Exception as e:
        print('[ERROR]: ' + str(e))

def run_Il2CppDump(apk:APK_Info):
    '''
    Run Il2CppDumpper over Unity APKs
    '''
    if not os.path.exists(f'{apk.decompiled_app_path}\\dumpped'):
        os.system(f'powershell.exe mkdir {apk.decompiled_app_path}\\dumpped')

    libil2cpp_path = f'{apk.decompiled_app_path}resources\\lib\\{apk.arch}\\libil2cpp.so'
    global_metadata_path =  f'{apk.decompiled_app_path}resources\\assets\\bin\\Data\\Managed\\Metadata\\global-metadata.dat'

    command = f'powershell.exe Il2CppDumper.exe {libil2cpp_path} {global_metadata_path} {apk.decompiled_app_path}dumpped'
    print(f'Running Il2CppDumpper for {apk.apk_file_name}...')
    process = subprocess.Popen(['Il2CppDumper.exe',libil2cpp_path,global_metadata_path,f'{apk.decompiled_app_path}dumpped'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()
    process.wait()
    
    if not os.path.exists(f'{apk.decompiled_app_path}\\dumpped\\DummyDll'):
        message = stdout.decode()
        error = message[message.find('ERROR'):]
        error = error[:error.find('\r\n')].replace('ERROR:','').strip()
        apk.error = error
        return False
    return True


def run_tests(apk:APK_Info):
    
    print(f'Starting analysis of {apk.apk_name}')
    
    result = subprocess.run('wsl ls ' + transfor_to_wsl_path(apk.path_to_dlls), shell=True, check=True, capture_output=True, text=True)
    dlls = result.stdout.strip().splitlines()
    
    n_dlls = len(dlls)
    for counter, dll in enumerate(dlls):
        if dll[-4:] == '.dll':
            test_get_classes = Test('dll_class_discover.py', [apk.results_path+'dll_classes\\',dll[:len(dll)-4]] ,dll)
            test_get_classes.run(apk)
            print(f'{counter+1}/{n_dlls} DLLs analyzed', end='\r')

    apk.android_sdks, apk.dll_sdks = extract_sdks(apk)
    
    print(f'The analysis of  {apk.apk_name} has finished')

def transfor_to_wsl_path(path):
    return path.replace('\\','/').replace('C:','/mnt/c/').replace('//','/')

def add_to_total_android_sdks(android_sdks):
    global total_android_sdks
    for sdk in android_sdks:
        if sdk in total_android_sdks.keys():
            total_android_sdks[sdk] += 1
        else:
            total_android_sdks[sdk] = 1
def add_to_total_dll_sdks(dlls):
    global total_dll_sdks
    for dll in dlls:
        if dll in total_dll_sdks.keys():
            total_dll_sdks[dll] += 1
        else:
            total_dll_sdks[dll] = 1

def extract_sdks(apk:APK_Info):
    '''
    Extract the SDKs from the APK
    '''
    
    android_sdks = get_android_sdks(apk)
    dll_sdks = get_dll_sdks(apk)
    
    return android_sdks, dll_sdks

def is_in_native_owners(sdk:str):
    for owner in native_owners:
        if owner.lower() in sdk.lower():
            return True
    return False

def check_unity_runtime_environment(apk:APK_Info):
    '''
    It checks the runtime environment of the Unity APKs
    '''
    if os.path.exists(f'{apk.decompiled_app_path}resources\\lib\\{apk.arch}\\libil2cpp.so'):
        apk.set_runtime_environment('IL2CPP')
    else:
        apk.set_runtime_environment('Mono')
