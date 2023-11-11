import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import re
import os

class NMRSpectr():
    def __init__(self, name_file, cursor, add_new=True):
        self.data = []
        self.name_file = os.path.abspath(name_file)
        self.cursor = cursor
        self.ppm_flag = False
        self.secondst_flag = False
        self.spectral_width = 0.0
        self.spectrometer_frequency = 0.0
        self.read_file()
        if add_new:
            self.add_file_in_database()
        self.first_coloumn = self.type_spectr()
        self.df = pd.DataFrame(self.data, columns=[self.first_coloumn, 'Real', 'Imaginary'])
        if self.secondst_flag:
            self.furie_spectr()
        
    def add_file_in_database(self):
        self.cursor.execute(
            f"INSERT INTO table_spectr (name_file) VALUES ('{self.name_file}')")
        
    def watch_all_files_database(self):
        sql_request = "SELECT name_file FROM table_spectr WHERE type_spectr = 'NMR'"
        self.cursor.execute(sql_request)
        result = self.cursor.fetchall()
        print("ЯМР файлы в базе данных")
        for row in result:
            print(row[0])

    def read_file(self):
        with open(self.name_file, 'r') as file:
            lines = file.readlines()
            start = False
            for line in lines:
                if line.startswith('Spectral Width'): 
                    self.spectral_width = float(re.search(r'\d+\.\d+', line).group())
                if line.startswith('Spectrometer Frequency'): 
                    self.spectrometer_frequency = float(re.search(r'\d+\.\d+', line).group())
                if line.startswith('ppm') or line.startswith('Hz'):
                    self.ppm_flag = True
                if line.startswith('Secondst'):
                    self.secondst_flag = True
                if line.startswith('______') and (self.ppm_flag or self.secondst_flag):
                    start = True
                    continue
                if start and line.strip(): 
                    values = line.split('\t')
                    self.data.append([float(value) for value in values if value.strip()]) 
                
    def type_spectr(self):
        if self.ppm_flag:
            return 'ppm'
        if self.secondst_flag:
            return 'Secondst'

    def draw_spectr(self, flag_save):
        if self.ppm_flag:
            name_x = self.first_coloumn
            y_axis = self.df[self.first_coloumn].to_numpy()
            x_axis = self.df['Real'].to_numpy()
        else:
            name_x = 'Hz'
            y_axis = self.df['freq_axis_shifted'].to_numpy()
            x_axis = self.df['spectrum'].to_numpy()
        plt.figure(figsize=(10, 6))
        plt.plot(y_axis, x_axis, linewidth=0.5, color='black')
        plt.xlabel(name_x)
        plt.title(f'ЯМР график {self.name_file}')
        plt.grid(color='r', linestyle='-', linewidth=0.1)
        plt.yticks([])
        plt.gca().invert_xaxis()
        if flag_save:
            file_name = f"NMR_spectr_{self.name_file[:-4]}.png"
            plt.savefig(file_name, format='png')
            print(f"Спектр ЯМР был сохранен в файле {file_name}")
        plt.show()
    
    
    def information_spectr(self):
        self.max_peak()
        print(f'Спектральная ширина (Гц) {self.spectral_width}')
        print(f'Частота спектрометра (МГц) {self.spectrometer_frequency}')
        
        
    def max_peak(self):
        idx_max_real = self.df['Real'].idxmax()
        point_of_max_real = self.df.at[idx_max_real, self.first_coloumn ]
        print(f'Пик {point_of_max_real}')
        

    def furie_spectr(self):
        self.df = self.df.sort_values(by='Secondst')
        FID = self.df['Real'] + 1j * self.df['Imaginary'] 
        dt = self.df['Secondst'][2] - self.df['Secondst'][1]
        fs = 1 / dt
        self.df['spectrum'] = np.abs(np.fft.fft(FID))
        self.df['freq_axis_shifted'] = np.fft.fftfreq(len(self.df), 1/fs)
        self.first_coloumn = 'freq_axis_shifted'
        print(f"Данные файла {self.name_file} были апрксимированы с использованием преобразования Фурье")

