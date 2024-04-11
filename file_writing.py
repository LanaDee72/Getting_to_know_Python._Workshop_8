'''
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной
'''

from os.path import exists
from csv import DictReader, DictWriter

class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt

class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt
def get_info():
    is_valid_first_name = False
    while not is_valid_first_name:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Не валидное имя")
            else:
                is_valid_first_name = True
        except NameError as err:
            print(err)
            continue

    is_valid_last_name = False
    while not is_valid_last_name:
        try:
            last_name = input("Введите фамилию: ")
            if len(last_name) < 2:
                raise NameError("Не валидная фамилия")
            else:
                is_valid_last_name = True
        except NameError as err:
            print(err)
            continue

    is_valid_patronymic = False
    while not is_valid_patronymic:
        try:
            patronymic = input("Введите отчество: ")
            if len(patronymic) < 2:
                raise NameError("Не валидное отчество")
            else:
                is_valid_patronymic = True
        except NameError as err:
            print(err)
            continue

    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера")
            else:
                is_valid_phone = True
        except ValueError:
            print("Не валидный номер!!!")
            continue
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, last_name, patronymic, phone_number]


def create_file(file_name):
    # with - Менеджер контекста
    with open(file_name, "w", encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Отчество', 'Телефон'])
        f_writer.writeheader()


def read_file(file_name):
    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name, lst):
    res = read_file(file_name)
    for el in res:
        if el["Телефон"] == str(lst[3]):
            print("Такой телофон уже есть")
            return

    obj = {"Имя": lst[0], "Фамилия": lst[1], "Отчество": lst[2], "Телефон": lst[3]}
    res.append(obj)
    with open(file_name, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Отчество', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)

def find_info(file_name):
    '''
    Поиск контакта
    '''
    print(f'1 - поиск по имени\n'
    f'2 - поиск по фамилии\n'
    f'3 - поиск по имени и фамилии')
    num = int(input(f'Введите критерий для поиска: '))
    res = read_file(file_name)
    find_res = []
    if num == 1:
        find_name = input('Введите имя для поиска: ').lower()
        for el in res:
            if el["Имя"].lower() == find_name:
                find_res.append(el)
        if len(find_res) == 0:
            return ['Пользователь не найден']
        return find_res
    elif num == 2:
        find_name = input('Введите фамилию для поиска: ').lower()
        for el in res:
            if el["Фамилия"].lower() == find_name:
                find_res.append(el)
        if len(find_res) == 0:
            return ['Пользователь не найден']
        return find_res
    if num == 3:
        find_name = input('Введите имя и фамилию для поиска: ').lower().split()
        for el in res:
            if el["Имя"].lower() == find_name[0] and el["Фамилия"].lower() == find_name[1]:
                find_res.append(el)
        if len(find_res) == 0:
            return ['Пользователь не найден']
        return find_res

def replace_info(old_info, new_number):
    '''
    Смена старого номера телефона на новый
    '''
    res = [value for value in old_info[0].values()]
    res[3] = new_number
    return res

def change_info(file_name):
    '''
    Изменение номера телефона
    '''
    find = find_info(file_name)
    if find == ['Пользователь не найден']:
        return ['Пользователь не найден. Повторите попытку']
    elif len(find) != 1:
        return ['Найдено несколько пользователей. Повторите попытку']
    elif len(find) == 1:
        is_valid_phone = False
        while not is_valid_phone:
            try:
                phone_number = int(input("Введите номер: "))
                if len(str(phone_number)) != 11:
                    raise LenNumberError("Неверная длина номера")
                else:
                    is_valid_phone = True
            except ValueError:
                print("Не валидный номер!!!")
                continue
            except LenNumberError as err:
                print(err)
                continue
        new_info = replace_info(find, phone_number)
        write_file(file_name, new_info)
        delete_for_change(file_name, find[0]['Телефон'])
        return

def delete(file_name):
    '''
    Удаление контакта
    '''
    find = find_info(file_name)
    if find == ['Пользователь не найден']:
        return ['Пользователь не найден. Повторите попытку']
    elif len(find) != 1:
        return ['Найдено несколько пользователей. Повторите попытку']
    elif len(find) == 1:
        number = find[0]['Телефон']
    res = read_file(file_name)
    with open(file_name, "r+", encoding='utf-8') as data:
        data.truncate(28)
    for i in res:
        info = [value for value in i.values()]
        if number in info:
            continue
        write_file(file_name, info)

def delete_for_change(file_name, number):
    '''
    Удаление старого контакта при изменении номера
    '''
    res = read_file(file_name)
    with open(file_name, "r+", encoding='utf-8') as data:
        data.truncate(28)
    for i in res:
        info = [value for value in i.values()]
        if number in info:
            continue
        write_file(file_name, info)

def copy_from_file(file_name, file_name_from_copy):
    '''
    Копирование строки из одного файла в другой
    '''
    res_file_copy = read_file(file_name_from_copy)
    is_valid_string = True
    while is_valid_string:
        string = int(input('Введите номер строки для копирования: '))
        if string == 0 or string > len(res_file_copy[0]):
            print('Неверный номер строки')
        else:
            is_valid_string = False
    res_copy = [[value for value in i.values()] for i in res_file_copy]
    write_file(file_name, res_copy[string - 1])

file_name = 'phone.txt'


def main():
    while True:
        command = input("Введите команду: ")
        if command == 'q':          # Выйти
            break
        elif command == 'w':        # Записать
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == 'r':        # Прочитать
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            print(*read_file(file_name))
        elif command == 'f':        # Найти
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            print(*find_info(file_name))
        elif command == 'ch':        # Изменить
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            change_info(file_name)
        elif command == 'd':        # Удалить
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            delete(file_name)
        elif command == 'c':        # Копировать
            file_name_from_copy = 'phone2.txt'
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            if not exists(file_name_from_copy):
                print("Файл отсутствует. Создайте его")
                continue
            copy_from_file(file_name, file_name_from_copy)

main()