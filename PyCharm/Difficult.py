#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os.path
import click
from datetime import date


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



@click.group()
@click.pass_context
def main(ctx):
    """
    Главная функция программы.
    """
    ctx.ensure_object(dict)

@main.command()
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
@click.option('--name', prompt='Введите ФИО')
@click.option('--tel', prompt='Введите номер телефона', type=int)
@click.option('--year', prompt='Введите год')
def add(ctx, filename, name, tel, year):
    """
    Добавить нового человека.
    """
    if os.path.exists(filename):
        people = load_workers(filename)
    else:
        people = []

    people = add_man(people, name, tel, year)
    save_workers(filename, people)


@main.command()
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
def list(ctx, filename):
    """
    Отобразить список лбдей.
    """
    if os.path.exists(filename):
        people = load_workers(filename)
        list_man(people)


@main.command()
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
@click.option('--select', prompt='Введите имя')
def select(ctx, filename, name):
    """
    Выбрать человека.
    """
    if os.path.exists(filename):
        people = load_workers(filename)
        selected = select_man(people, name)
        list_man(selected)




if __name__ == '__main__':
    main()
