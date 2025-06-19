import subprocess
import os
import re
from os import path as os_path
import pickle
import traceback

from matplotlib import pyplot as plt
from modules.configuration import *
from modules.Test import Test
from modules.APK_Info import APK_Info
from modules.freq_diagrams import *
from analysis.modules.analizer import *

apk_path = ''
apk_list = list()

total_third_party_libs = dict()
total_unity_libs = dict()
total_unreal_libs = dict()
total_native_libs = dict()
total_unity_bin = dict()
total_unreal_bin = dict()
total_native_bin = dict()
total_third_party_binaries = dict()
total_permissions_by_owner = dict()
native_libs = list()



def data_analysis_sdks():
    graphs_paths = os.listdir('.\\graphs\\freq')
    for file in graphs_paths:
        os.remove(f'.\\graphs\\freq\\{file}')
        
    dict_android_sdks = dict()
    dict_dlls_sdks = dict()
    dict_android_sdks_reversed  = dict()
    dict_dlls_sdks_reversed = dict()
    dict_android_sdks_filtered = dict()
    dict_dlls_sdks_filtered = dict()
    dict_android_sdks_reversed_filtered  = dict()
    dict_dlls_sdks_reversed_filtered = dict()
    
    for apk in apk_list:
        
        if apk.is_analyzed and apk.error == None and apk.is_unity:
            fd = open('.\\graphs\\freq\\\dex_sdks.csv', 'a')
            fd_reversed = open('.\\graphs\\freq\\dex_sdks_reverse.csv', 'a')

            for android_sdk in apk.android_sdks:
                
                if android_sdk in dict_android_sdks.keys():
                    dict_android_sdks[android_sdk] += 1
                else:
                    dict_android_sdks[android_sdk] = 1
                
                if not is_in_native_owners(android_sdk):
                    if android_sdk in dict_android_sdks_filtered.keys():
                        dict_android_sdks_filtered[android_sdk] += 1
                    else:
                        dict_android_sdks_filtered[android_sdk] = 1
                
                if apk.apk_name not in dict_android_sdks_reversed.keys():
                    dict_android_sdks_reversed[apk.apk_name] = 1
                else:
                    dict_android_sdks_reversed[apk.apk_name] += 1
                
                if not is_in_native_owners(android_sdk):   
                    if apk.apk_name not in dict_android_sdks_reversed_filtered.keys():
                        dict_android_sdks_reversed_filtered[apk.apk_name] = 1
                    else:
                        dict_android_sdks_reversed_filtered[apk.apk_name] += 1
                        
                fd.write(f'{android_sdk},{apk.apk_name}\n')
                fd_reversed.write(f'{apk.apk_name},{android_sdk}\n')
            
            fd.close()
            fd_reversed.close()
            
            with open('.\\graphs\\freq\\freq_dexs.csv','w') as fd:
                sorted_dict_android_sdks = dict(sorted(dict_android_sdks.items(), key=lambda item: item[1], reverse=True))
                for sdk in sorted_dict_android_sdks.keys():
                    fd.write(f'{sdk},{sorted_dict_android_sdks[sdk]}\n')
            
            fd = open('.\\graphs\\freq\\dll_sdks.csv', 'a')
            fd_reversed = open('.\\graphs\\freq\\dll_sdks_reverse.csv', 'a')     
            
            for dll_sdk in apk.dll_sdks:
                
                if dll_sdk in dict_dlls_sdks.keys():
                    dict_dlls_sdks[dll_sdk] += 1
                else:
                    dict_dlls_sdks[dll_sdk] = 1
                
                if not is_in_native_owners(dll_sdk):
                    if dll_sdk in dict_dlls_sdks_filtered.keys():
                        dict_dlls_sdks_filtered[dll_sdk] += 1
                    else:
                        dict_dlls_sdks_filtered[dll_sdk] = 1
                
                if apk.apk_name not in dict_dlls_sdks_reversed.keys():
                    dict_dlls_sdks_reversed[apk.apk_name] = 1
                else:
                    dict_dlls_sdks_reversed[apk.apk_name] += 1
                
                if not is_in_native_owners(dll_sdk):
                    if apk.apk_name not in dict_dlls_sdks_reversed_filtered.keys():
                        dict_dlls_sdks_reversed_filtered[apk.apk_name] = 1
                    else:
                        dict_dlls_sdks_reversed_filtered[apk.apk_name] += 1
                fd.write(f'{dll_sdk},{apk.apk_name}\n')
                fd_reversed.write(f'{apk.apk_name},{dll_sdk}\n')
            
            fd.close()
            fd_reversed.close()
            
            with open('.\\graphs\\freq\\freq_dlls.csv','w') as fd:
                sorted_dict_dlls_sdks = dict(sorted(dict_dlls_sdks.items(), key=lambda item: item[1], reverse=True))
                for sdk in sorted_dict_dlls_sdks.keys():
                    fd.write(f'{sdk},{sorted_dict_dlls_sdks[sdk]}\n')
        
    for i in range(3):
        
        bars = 10 * (i+1)
        plot_freq_graph(dict_android_sdks, f'Frequency of Android SDKs (TOP-{bars})', x_name='dex', y_name='APKs', bars=bars)
        plot_freq_graph(dict_dlls_sdks, f'Frequency of DLLs SDKs (TOP-{bars})', x_name='dlls', y_name='APKs', bars=bars)
        plot_freq_graph(dict_android_sdks_reversed, f'Number of Android SDKs (TOP-{bars})_reversed', y_name='dex', x_name='APKs', bars=bars)
        plot_freq_graph(dict_dlls_sdks_reversed, f'Number of DLLs SDKs (TOP-{bars})_reversed', y_name='dlls', x_name='APKs', bars=bars)
        
        plot_freq_graph(dict_android_sdks_filtered, f'Frequency of Android SDKs (TOP-{bars}) [Filtered]', x_name='dex', y_name='APKs', bars=bars)
        plot_freq_graph(dict_dlls_sdks_filtered, f'Frequency of DLLs SDKs (TOP-{bars}) [Filtered]', x_name='dlls', y_name='APKs', bars=bars)
        plot_freq_graph(dict_android_sdks_reversed_filtered, f'Number of Android SDKs (TOP-{bars})_reversed [Filtered]', y_name='dex', x_name='APKs', bars=bars)
        plot_freq_graph(dict_dlls_sdks_reversed_filtered, f'Number of DLLs SDKs (TOP-{bars})_reversed [Filtered]', y_name='dlls', x_name='APKs', bars=bars)
    
    
    with open('.\\graphs\\freq\\\dll_sdks.csv', 'r') as fd:    
        total_dll_sdks_list = fd.readlines()
    with open('.\\graphs\\freq\\\dll_sdks.csv', 'w') as fd:
        ordered_dll_sdks_list = sorted(total_dll_sdks_list, key = str.lower) 
        for line in ordered_dll_sdks_list:
            parts = line.strip().split(',')
            sdk = parts[0]
            app_name = parts[1]
            fd.write(f'{sdk},{app_name}\n')
                
    with open('.\\graphs\\freq\\dll_sdks_reverse.csv', 'r') as fd:    
        total_dll_sdks__reversed_list = fd.readlines()
    with open('.\\graphs\\freq\\dll_sdks_reverse.csv', 'w') as fd:
        ordered_dll_sdks__reverse_list = sorted(total_dll_sdks__reversed_list, key = str.lower)
        for line in ordered_dll_sdks__reverse_list:
            parts = line.strip().split(',')
            app_name = parts[0]
            sdk = parts[1]
            fd.write(f'{app_name},{sdk}\n')
            
    with open('.\\graphs\\freq\\\dex_sdks.csv', 'r') as fd:    
        total_android_sdks_list = fd.readlines()
    with open('.\\graphs\\freq\\\dex_sdks.csv', 'w') as fd:
        ordered_android_sdks_list = sorted(total_android_sdks_list, key = str.lower)
        for line in ordered_android_sdks_list:
            parts = line.strip().split(',')
            sdk = parts[0]
            app_name = parts[1]
            fd.write(f'{sdk},{app_name}\n')
                
    with open('.\\graphs\\freq\\dex_sdks_reverse.csv', 'r') as fd:    
        total_android_sdks_reversed_list = fd.readlines()
    with open('.\\graphs\\freq\\dex_sdks_reverse.csv', 'w') as fd:
        ordered_android_sdks_reversed_list = sorted(total_android_sdks_reversed_list, key = str.lower)  
        for line in ordered_android_sdks_reversed_list:
            parts = line.strip().split(',')
            app_name = parts[0]
            sdk = parts[1]
            fd.write(f'{app_name},{sdk}\n') 

    print(f'SDKs Data Analisys Finished [END] --> {len(dict_android_sdks_reversed) + len(dict_dlls_sdks_reversed)}')


def update_object(apk):
    new_base_apk_object = APK_Info(apk.apk_name,apk.apk_path)
    is_modified = False
    for attr_name, attr_value in new_base_apk_object.__dict__.items():
        
        if not hasattr(apk, attr_name):
                setattr(apk, attr_name, attr_value)
                is_modified = True
                print(f"New attribute of the APK '{apk.apk_name}' --> {attr_name}: {attr_value}")
    if is_modified: save_state(apk)

def load_state():

    '''
    Load the state of the analysis. It populate the list of apk objects in the different directories.
        1- It load the possible existent APK and check wheter they are analyzed or not to add those that are not to the ToDO list.
        2- It checks for new APKs in the 'APKs' folder and create the structure in the directories for this APK and create an empty APK Object.
    '''

    apk_dirs = os.listdir('.\\Data')
    todo_list = list()
    del apk_dirs[apk_dirs.index('APKs')]

    for apk_dir in apk_dirs:
        
        with open(f'.\\Data\\{apk_dir}\\{apk_dir}_object.txt', 'rb') as fd:
            apk = pickle.load(fd)
        update_object(apk)
        apk_list.append(apk)
        if not apk.is_analyzed:
            todo_list.append(apk)
    
    new_apks = os.listdir('.\\Data\\APKs')
    for apk in new_apks:
        
        apk_name = apk.replace('.apk','')
        new_apk_name = apk_name.replace('.','_') #To remove every '.' in the mane
        apk_path = '.\\Data\\' + new_apk_name + '\\'
        apk = APK_Info(new_apk_name, apk_path)

        os.system('mkdir .\\Data\\' + apk.apk_name)
        os.system('mkdir .\\Data\\' + apk.apk_name + '\\results')
        os.system('mkdir .\\Data\\' + apk.apk_name + '\\results\\dll_classes')
        os.system(f'powershell.exe mv .\\Data\\APKs\\{apk_name}.apk  .\\Data\\{apk.apk_name}\\{apk.apk_file_name}')
        save_state(apk)
        apk_list.append(apk)
        todo_list.append(apk)
    
    return apk_list, todo_list 

def save_state(apk:APK_Info):
    print(f'Saving state of {apk.apk_name}')
    with open(apk.apk_path + apk.apk_name + '_object.txt', 'wb') as fd:
        pickle.dump(apk, fd)

if __name__ == '__main__':
    apk_list, todo_list = load_state()
    n_apks = len(apk_list)

    for counter,apk in enumerate(apk_list):
        print(f'Analyzing {apk.apk_name}...')
        apk:APK_Info
        if apk.is_unity: 
            print(apk.apk_unity_version)


        decompile_app(apk)
        
        apk.android_sdks, apk.dll_sdks = extract_sdks(apk)
        #save_state(apk)
        if not apk.is_analyzed and apk.error == None:
            
            apk.is_unity, apk.apk_unity_version = check_unity_version(apk)
            if not apk.is_unity: apk.is_unreal_engine = check_unreal(apk)
            
            
            
            if apk.is_unity:
                check_unity_runtime_environment(apk)
                if apk.runtime_environment == 'IL2CPP': is_successful = run_Il2CppDump(apk)
                
                if is_successful: 
                    run_tests(apk)
                    apk.is_analyzed = True    

                save_state(apk)
                print(f'{apk.apk_name} has been analyzed [END OF THE ANALISYS]--> {counter+1}/{n_apks}')
            else:
                print(f'{apk.apk_name} is not a Unity APK [END OF THE ANALISYS] --> {counter+1}/{n_apks}')
            
        else: print(f'{apk.apk_name} has been already analyzed [END OF THE ANALISYS] --> {counter+1}/{n_apks}')
            
    #----------------Analysis----------------

    print('Starting the Data Analysis of the SDKs')
    data_analysis_sdks()
    