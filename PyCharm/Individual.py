#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path


def add_man(students, name, tel, year):
    """
    Добавление студента в список
    """
    students.append(
        {
            "name": name,
            "tel": tel,
            "year": year
        }
    )
    return students


def list_man(people):
    """
    Вывод людей
    """

    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 12
    )
    print(line)
    print(
        '| {:^4} | {:^30} | {:^20} | {:^12} |'.format(
            "№",
            "Ф.И.О.",
            "Телефон",
            "Год рождения"
        )
    )
    print(line)

    for idx, man in enumerate(people, 1):
        print(
            '| {:>4} | {:<30} | {:<20} | {:>12} |'.format(
                idx,
                man.get('name', ''),
                man.get('tel', ''),
                str(man.get('year', 0))
            )
        )
    print(line)


def select_man(arr, person):
    """
    Вывод конкретных людей
    """
    result = []
    for employee in arr:
        if employee.get('name', person).lower() == person.lower():
            result.append(employee)

    # Возвратить список выбранных работников.
    return result


def display_man(staff):
    if staff:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 12
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^12} |'.format(
                "№",
                "Ф.И.О.",
                "Телефон",
                "Год рождения"
            )
        )
        print(line)
        for idx, worker in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>12} |'.format(
                    idx,
                    worker.get('name', ''),
                    worker.get('tel', ''),
                    str(worker.get('date', 0))
                )
            )
        print(line)
    else:
        print("Список пуст")

def help_man():
    print("Список команд:\n")
    print("add - добавить человека;")
    print("list - вывести список людей;")
    print("select <имя> - запросить людей с этим именем;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")

def save_workers(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4, default=str)


def load_workers(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)



def main(command_line=None):
    """
    Главная функция
    """
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="Имя файла"
    )
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Добавление студента"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        type=str,
        required=True,
        help="ФИО студента"
    )
    add.add_argument(
        "-t",
        "--tel",
        action="store",
        type=int,
        help="Номер телефона"
    )
    add.add_argument(
        "-y",
        "--year",
        action="store",
        type=str,
        required=True,
        help="Год поступления"
    )

    _ = subparsers.add_parser(
        "list",
        parents=[file_parser],
        help="Отобразить список студентов"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Отобразить нужного студента"
    )

    select.add_argument(
        "-p",
        "--person",
        action="store",
        type=str,
        required=True,
        help="person"
    )

    args = parser.parse_args(command_line)

    is_dirty = False
    if os.path.exists(args.filename):
        students = load_workers(args.filename)
    else:
        students = []

    if args.command == "add":
        students = add_man(
            students,
            args.name,
            args.tel,
            args.year
        )
        is_dirty = True

    elif args.command == "list":
        list_man(students)

    elif args.command == "select":
        filter_list = select_man(students, args.person)
        display_man(filter_list)

    if is_dirty:
        save_workers(args.filename, students)


if __name__ == '__main__':
    main()
