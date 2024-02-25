from scipy import stats
from .models import *
import numpy as np


def analyze_ir_spectrum_correlation(spectr1, spectr2):
    value_x1_str = spectr1.spectr.values.values_x
    value_x2_str = spectr2.spectr.values.values_x
    dic = {}

    data_1 = np.fromstring(value_x1_str,  dtype=float, sep=' ')
    data_2 = np.fromstring(value_x2_str, dtype=float,  sep=' ')

    correlation_coefficient, _ = stats.pearsonr(data_1, data_2)
    t_stat, p_value = stats.ttest_ind(data_1, data_2)

    dic['Коэффициент корреляции Пирсона'] = correlation_coefficient
    dic['t-критерий'] = t_stat
    dic['p-значение'] = p_value

    return dic
