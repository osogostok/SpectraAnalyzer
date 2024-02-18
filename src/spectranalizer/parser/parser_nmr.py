import zipfile
import os
import matplotlib.pyplot as plt
import nmrglue as ng
import numpy as np

class NMRSpectr():
    def __init__(self, zip_file_path):
        self.temp_folder = "./temp_extracted_data"
        self.zip_file_path = zip_file_path
        self.dic = None
        self.data = None
        self.ppm_scale = None
        self.postcorr_frq = None
        self.values_x = None
        self.values_y = None
        
        self.read_zip()
        self.precess_pdata()
        self.ppm()
        
    def read_zip(self):
        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            os.makedirs(self.temp_folder, exist_ok=True)
            zip_ref.extractall(self.temp_folder)
    
    def precess_pdata(self):
        for root, dirs, files in os.walk(self.temp_folder):
            if "pdata" in dirs:
                pdata_folder = os.path.join(root, "pdata", "1")
                if os.path.isdir(pdata_folder):
                    self.dic, self.data = ng.bruker.read_pdata(pdata_folder, scale_data=True)
                    self.values_x = ' '.join(map(str, self.data))
                    # print(self.values_x)
                    # self.values_y = np.array2string(self.data[:,0])
    
    def ppm(self):
        udic = ng.bruker.guess_udic(self.dic, self.data)
        uc = ng.fileiobase.uc_from_udic(udic)
        self.ppm_scale = uc.ppm_scale()
        self.values_y = ' '.join(map(str, self.ppm_scale))
        
    def fft(self):
        # precorr_time =  ng.bruker.remove_digital_filter(self.dic, self.data)
        # precorr_frq = ng.proc_base.fft(precorr_time)
        # precorr_frq = ng.proc_autophase.autops(precorr_frq, 'peak_minima')
        
        self.postcorr_frq = ng.proc_base.fft(self.data)
        self.postcorr_frq = ng.bruker.remove_digital_filter(self.dic, self.postcorr_frq, post_proc=True)
        self.postcorr_frq = ng.proc_autophase.autops(self.postcorr_frq, 'acme')
    
    def png_save(self):
        plt.plot(self.ppm_scale, self.data)
        plt.xlabel('ppm')
        plt.ylabel('Интенсивность')
        plt.title('График данных ЯМР с осями в ppm')
        plt.tight_layout()
        plt.savefig('dig_filter_remove.png')

