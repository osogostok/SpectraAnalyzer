from model.model_nmr_spectr import NMRSpectr
from model.model_ir_spectr import IRSpectr
from model.model_convergence import convergence_check
import argparse
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from prettytable import PrettyTable

load_dotenv()
DATABASE = os.getenv('DATABASE')
PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
PASSWORD = os.getenv('PASSWORD')
USER_DATABASE = os.getenv('USER_DATABASE')


def connection_database():
    connection = psycopg2.connect(
        user=USER_DATABASE, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return connection


def is_txt_file(file_name):
    if not os.path.exists(file_name):
        raise argparse.ArgumentTypeError(f"{file_name} не является файлом.")
    if not file_name[-4:] == '.txt':
        raise argparse.ArgumentTypeError(
            "Файл должен иметь расширение '.txt'.")
    return file_name


def is_xlsx_file(file_name):
    if not os.path.exists(file_name):
        raise argparse.ArgumentTypeError(f"{file_name} не является файлом.")
    if not file_name[-5:] == '.xlsx':
        raise argparse.ArgumentTypeError(
            "Файл должен иметь расширение '.xlsx'.")
    return file_name


def read_arg():
    parser = argparse.ArgumentParser(description='Great Description')
    parser.add_argument('-n', '--nmr_file',
                        type=is_txt_file,  help="Тип файла .txt")
    parser.add_argument('-i', '--ir_file',
                        type=is_xlsx_file, help="Тип файла .xlsx")
    parser.add_argument('-d', '--draw', action='store_true',
                        help="Посмотреть спектр")
    parser.add_argument('-s', '--save', action='store_true',
                        help="Сохранить спект в виде изображения")
    parser.add_argument('-c', '--convergence', nargs=2,
                        help="Расчитать коэффицент корреляции между файлами")
    parser.add_argument('-f', '--files', action='store_true',
                        help="Вывести файлы из базы данных")
    args = parser.parse_args()
    return args


def select_files(cursor):
    sql_request = "SELECT name_file, type_spectr FROM table_spectr"
    cursor.execute(sql_request)
    result = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["Имя файла", "Тип спектра"]
    for row in result:
        table.add_row([row[0], row[1]])
    print(table)


def main(cursor):
    arg = read_arg()
    if arg.nmr_file:
        spectr = NMRSpectr(arg.nmr_file, cursor)
        if arg.draw:
            spectr.draw_spectr(arg.save)
    if arg.ir_file:
        ir_spectr = IRSpectr(arg.ir_file, cursor)
        if arg.draw:
            ir_spectr.draw_spectr(arg.save)
    if arg.convergence:
        convergence_check(arg.convergence[0], arg.convergence[1], cursor)
    if arg.files:
        select_files(cursor)


if __name__ == '__main__':
    try:
        connection = connection_database()
        cursor = connection.cursor()
        main(cursor)
    except psycopg2.Error as e:
        if "File exist" in str(e):
            print("Файл уже существует.")
        else:
            print("Произошла ошибка вставки:", e)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
