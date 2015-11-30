# -*- coding: utf-8 -*-

import codecs
import xml.etree.ElementTree
import os
from os import path


TASK_BASE_PATH = 'task_base'
TESTS = 'tests'
STATEMENT = 'statement.xml'
IN_EXTENSION = '.in'
OUT_EXTENSION = '.out'
TUTORIAL = 'tutorial'
TXT_EXTENSION = '.txt'
CHECKER = 'checker'


TITLE_TAG = 'title'
MEMORY_LIMIT_TAG = 'memory_limit'
TIME_LIMIT_TAG = 'time_limit'
TEXT_TAG = 'text'
INPUT_FORMAT_TAG = 'input_format'
OUTPUT_FORMAT_TAG = 'output_format'
FIRST_TEST_NOTE_TAG = 'first_test_note'
SECOND_TEST_NOTE_TAG = 'second_test_note'
TEXT_NOTE_TAG = 'text_note'


def get_tutorial_html(task_id):
    task_path = TASK_BASE_PATH + os.sep + str(task_id)
    tutorial_path = task_path + os.sep + TUTORIAL + TXT_EXTENSION

    with open(tutorial_path, 'r', encoding='utf-8') as tutorial_file:
        tutorial_text = tutorial_file.read()

    tutorial_html = '<p align="center"><b>Обучающие материалы</b></p>\n'
    tutorial_html += '<p>' + tutorial_text + '</p>\n'

    return tutorial_html


def get_task_path(task_id):
    return TASK_BASE_PATH + os.sep + str(task_id)


def get_statement_path(task_id):
    return get_task_path(task_id) + os.sep + STATEMENT


def get_tests_path(task_id):
    return get_task_path(task_id) + os.sep + TESTS


def get_str_test_number(test_number):
    if test_number < 10:
        return '00' + str(test_number)
    if test_number < 100:
        return '0' + str(test_number)
    return str(test_number)


def get_input_test_path(task_id, test_number):
    return get_tests_path(task_id) + os.sep + get_str_test_number(test_number) + IN_EXTENSION


def get_output_test_path(task_id, test_number):
    return get_tests_path(task_id) + os.sep + get_str_test_number(test_number) + OUT_EXTENSION


def get_statement_xml_tree_root(statement_path):
    return xml.etree.ElementTree.parse(statement_path).getroot()


def get_time_limit(task_id):
    statement_path = get_statement_path(task_id)
    root = get_statement_xml_tree_root(statement_path)
    return root.find(TIME_LIMIT_TAG).text


def get_memory_limit(task_id):
    statement_path = get_statement_path(task_id)
    root = get_statement_xml_tree_root(statement_path)
    return root.find(MEMORY_LIMIT_TAG).text


def get_task_title(task_id):
    statement_path = get_statement_path(task_id)
    root = get_statement_xml_tree_root(statement_path)
    return root.find(TITLE_TAG).text


def get_checker_path(task_id):
    return get_task_path(task_id) + os.sep + CHECKER


def get_task_html(task_id):
    task_path = get_task_path(task_id)
    statement_path = get_statement_path(task_id)
    tests_path = get_tests_path(task_id)
    first_test_input_path = get_input_test_path(task_id, 1)
    first_test_output_path = get_output_test_path(task_id, 1)
    second_test_input_path = get_input_test_path(task_id, 2)
    second_test_output_path = get_output_test_path(task_id, 2)

    root = get_statement_xml_tree_root(statement_path)

    title = root.find(TITLE_TAG).text
    memory_limit = root.find(MEMORY_LIMIT_TAG).text
    time_limit = root.find(TIME_LIMIT_TAG).text
    text = root.find(TEXT_TAG).text
    input_format = root.find(INPUT_FORMAT_TAG).text
    output_format = root.find(OUTPUT_FORMAT_TAG).text

    with codecs.open(first_test_input_path, 'r', encoding='utf-8') as first_test_input_file:
        first_test_input = first_test_input_file.read()
    with codecs.open(first_test_output_path, 'r', encoding='utf-8') as first_test_output_file:
        first_test_output = first_test_output_file.read()

    with codecs.open(second_test_input_path, 'r', encoding='utf-8') as second_test_input_file:
        second_test_input = second_test_input_file.read()
    with codecs.open(second_test_output_path, 'r', encoding='utf-8') as second_test_output_file:
        second_test_output = second_test_output_file.read()

    first_test_note = root.find(FIRST_TEST_NOTE_TAG).text
    second_test_note = root.find(SECOND_TEST_NOTE_TAG).text
    text_note = root.find(TEXT_NOTE_TAG).text

    title = title.strip()
    memory_limit = memory_limit.strip()
    time_limit = time_limit.strip()
    text = text.strip()
    input_format = input_format.strip()
    output_format = output_format.strip()
    first_test_input = first_test_input.strip()
    first_test_output = first_test_output.strip()
    second_test_input = second_test_input.strip()
    second_test_output = second_test_output.strip()
    first_test_note = first_test_note.strip()
    second_test_note = second_test_note.strip()
    text_note = text_note.strip()

    task_html = '<h2 align="center">' + title + '</h2>\n'
    task_html += '<p align="center">Ограничение по времени на тест: ' + time_limit + ' с</p>\n'
    task_html += '<p align="center">Ограничение по памяти на тест: ' + memory_limit + ' Мб</p>\n'
    task_html += '<p align="center"><b>Условие задачи</b></p>\n'
    task_html += '<p>' + text + '</p>\n'
    task_html += '<b>Формат входных данных:</b>\n'
    task_html += '<p>' + input_format + '</p>\n'
    task_html += '<b>Формат выходных данных:</b>\n'
    task_html += '<p>' + output_format + '</p>\n'
    task_html += '<b>Примеры тестов:</b>\n'
    task_html += \
        '<table style="width:100%">\n' + \
        '    <tr>\n' + \
        '        <td>Входные данные</td>\n' + \
        '    </tr>\n' + \
        '    <tr>\n' + \
        '        <td>' + first_test_input + '</td>\n' + \
        '    </tr>\n' + \
        '    <tr>\n' + \
        '        <td>Выходные данные</td>\n' + \
        '    </tr>\n' + \
        '    <tr>\n' + \
        '        <td>' + first_test_output + '</td>\n' + \
        '    </tr>\n' + \
        '</table>\n'
    task_html += \
        '<table style="width:100%">\n' + \
        '    <tr>\n' + \
        '        <td>Входные данные</td>\n' + \
        '    </tr>\n' + \
        '    <tr>\n' + \
        '        <td>' + second_test_input + '</td>\n' + \
        '    </tr>\n' + \
        '    <tr>\n' + \
        '        <td>Выходные данные</td>\n' + \
        '    </tr>\n' + \
        '    <tr>\n' + \
        '        <td>' + second_test_output + '</td>\n' + \
        '    </tr>\n' + \
        '</table>\n'
    if len(first_test_note) > 0:
        task_html += '<b>Примечание к первому тесту</b>\n'
        task_html += '<p>' + first_test_note + '</p>\n'
    if len(second_test_note) > 0:
        task_html += '<b>Примечание к второму тесту</b>\n'
        task_html += '<p>' + second_test_note + '</p>\n'
    if len(text_note) > 0:
        task_html += '<b>Примечание к условию задачи</b>\n'
        task_html += '<p>' + text_note + '</p>\n'

    return task_html


def get_tests_count(task_id):
    MAX_TEST_COUNT = 999
    test_count = 2
    while test_count + 1 <= MAX_TEST_COUNT and \
          os.path.isfile(get_input_test_path(task_id, test_count + 1)):
        test_count += 1
    return test_count