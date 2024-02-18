import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

class IRSpectr():
    def __init__(self, file_name):
        self.values_x = None
        self.values_y = None
        self.name_file = os.path.abspath(file_name)
        self.df = pd.read_excel(file_name, header=None, names=[
                                'Frequency', 'Absorption'])
        self.create_approximation()
        ' '.join(map(str, self.df['Frequency']))
        self.values_x = ' '.join(map(str, self.df['Frequency']))
        self.values_y = ' '.join(map(str, self.df['Absorption']))

    def create_approximation(self):
        max_value = np.array2string(self.df.Absorption.max())
        min_value = self.df.Absorption.min()
        data = []
        for x in self.df['Absorption']:
            value = (x - min_value)/(min_value + max_value)
            data.append(value)
        self.df['Approximation'] = data

        
        