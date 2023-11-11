from scipy import stats
from model.model_ir_spectr import IRSpectr


def select_type(file_name, cursor):
    sql_request = f"SELECT name_file FROM table_spectr WHERE name_file LIKE '%{file_name}%';"
    cursor.execute(sql_request)
    file = cursor.fetchall()
    if not file:
        raise Exception(f"Файла {file_name} нет в базе данных. Добавьте его")
    sql_request = f"SELECT type_spectr FROM table_spectr WHERE name_file = '{file[0][0]}';"
    cursor.execute(sql_request)
    return cursor.fetchall()[0][0]


def convergence_check(file_name_1, file_name_2, cursor):
    type_1 = select_type(file_name_1, cursor)
    type_2 = select_type(file_name_2, cursor)

    if type_1 != type_2:
        raise Exception("данные разного типа")
    if type_1 == 'IR':
        ir_spector_1 = IRSpectr(file_name_1, cursor, add_new=False)
        ir_spector_2 = IRSpectr(file_name_2, cursor, add_new=False)
        data_1 = ir_spector_1.df['Approximation']
        data_2 = ir_spector_2.df['Approximation']
    else:
        raise Exception(f"Файлы не ИК-спектры.")

    correlation_coefficient, _ = stats.pearsonr(data_1, data_2)
    print(f'Коэффициент корреляции Пирсона: {correlation_coefficient}')

    if correlation_coefficient < 0.05:
        print("Дисперсии существенно отличаются, гомогенность не подтверждена.")
    else:
        print("Дисперсии схожи, гомогенность подтверждена.")

    t_stat, p_value = stats.ttest_ind(data_1, data_2)
    print(f"t-критерий: {t_stat}, p-значение: {p_value}")

    if p_value < 0.05:
        print("Графики различаются.")
    else:
        print("Графики схожи.")
