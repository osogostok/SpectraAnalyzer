import pandas as pd
import os


class IRSpectr():
    def __init__(self, file_name):
        self.name_file = os.path.abspath(file_name)
        self.df = pd.read_excel(file_name, header=None, names=[
                                'Frequency', 'Absorption'])
        if not self._check_numeric_columns(['Frequency', 'Absorption']):
            raise ValueError("Data does not match pattern")
        self.create_approximation()
        self.values_y = ' '.join(map(str, self.df['Frequency']))
        self.values_x = ' '.join(map(str, self.df['Absorption']))

    def create_approximation(self):
        max_value = self.df['Absorption'].max()
        min_value = self.df['Absorption'].min()
        self.df['Approximation'] = (
            self.df['Absorption'] - min_value) / (min_value + max_value)

    def _check_numeric_columns(self, columns):
        return all(self.df[col].apply(self._is_numeric).all() for col in columns)

    @staticmethod
    def _is_numeric(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
