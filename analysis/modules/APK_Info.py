from modules.configuration import full_project_path

class APK_Info():
    '''
    APK Objecto to hold the analysis state.
    '''
    def __init__ (self, apk_name, apk_path):
        self.apk_name = apk_name
        self.apk_file_name = apk_name + '.apk'
        self.apk_path = full_project_path + apk_path[2:]
        self.results_path = self.apk_path + 'results\\'
        self.decompiled_app_path = None
        self.is_unity = False
        self.is_unreal_engine = False
        self.apk_unity_version = None
        self.runtime_environment = None
        self.path_to_dlls = None
        self.apk_classes = list()
        self.apk_functions = list()
        self.android_sdks = list()
        self.dll_sdks = list()
        self.apk_imports = list()
        self.is_analyzed = False
        self.arch = None 
        if not hasattr(self, 'error'):
            self.error = None
        self.error = None
    def set_runtime_environment(self, runtime_environment):
        self.runtime_environment = runtime_environment
        if self.runtime_environment == 'IL2CPP':
            self.path_to_dlls = self.apk_path + f'decompiled_{self.apk_name}\\dumpped\\DummyDll\\'
        else:
            self.path_to_dlls = self.apk_path + f'decompiled_{self.apk_name}\\resources\\assets\\bin\\Data\\Managed\\'  



