import pandas as pd
import matplotlib.pyplot as plt
import os


class IRSpectr():
    def __init__(self, file_name, cursor, add_new=True):
        self.name_file = os.path.abspath(file_name)
        self.cursor = cursor
        self.df = pd.read_excel(file_name, header=None, names=[
                                'Frequency', 'Absorption'])
        self.create_approximation()
        if add_new:
            self.add_file_in_database()

    def create_approximation(self):
        max_value = self.df.Absorption.max()
        min_value = self.df.Absorption.min()
        data = []
        for x in self.df['Absorption']:
            value = (x - min_value)/(min_value + max_value)
            data.append(value)
        self.df['Approximation'] = data

    def add_file_in_database(self):
        self.cursor.execute(
            f"INSERT INTO table_spectr (name_file) VALUES ('{self.name_file}')")

    def watch_all_files_database(self):
        sql_request = "SELECT name_file FROM table_spectr WHERE type_spectr = 'IR'"
        self.cursor.execute(sql_request)
        result = self.cursor.fetchall()
        print("ИК файлы в базе данных")
        for row in result:
            print(row[0])

    def draw_spectr(self, flag_save):
        x_axis = self.df['Frequency'].to_numpy()
        y_axis = self.df['Approximation'].to_numpy()
        plt.figure(figsize=(10, 6))
        plt.plot(x_axis, y_axis, linewidth=0.5, color='black')
        plt.xlabel('Частота см-1')
        plt.title(f'ИК-график {self.name_file}')
        plt.grid(color='r', linestyle='-', linewidth=0.1)
        plt.yticks([])
        plt.gca().invert_xaxis()
        plt.xticks(range(int(min(x_axis)), int(max(x_axis))+1, 200))
        plt.savefig(f"spectr_{self.name_file[:-5]}.png", format='png')
        if flag_save:
            file_name = "IR_spectr_{self.name_file[0:-5]}.png"
            plt.savefig(file_name, format='png')
            print(f"Спектр ИК был сохранен в файле {file_name}")
        plt.show()
        
        
        
        
