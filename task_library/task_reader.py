# -*- coding: utf-8 -*-

import codecs
import xml.etree.ElementTree

BASE_PATH = 'task_base'

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
    task_path = BASE_PATH + '/' + str(task_id)
    tutorial_path = task_path + '/tutorial.txt'

    with open(tutorial_path, 'r', encoding='utf-8') as tutorial_file:
        tutorial_text = tutorial_file.read()

    tutorial_html = '<p align="center"><b>Обучающие материалы</b></p>\n'
    tutorial_html += '<p>' + tutorial_text + '</p>\n'

    return tutorial_html

def get_task_html(task_id):
    task_path = BASE_PATH + '/' + str(task_id)
    statement_path = task_path + '/statement.xml'
    tests_path = task_path + '/tests'
    first_test_input_path = tests_path + '/001.in'
    first_test_output_path = tests_path + '/001.out'
    second_test_input_path = tests_path + '/002.in'
    second_test_output_path = tests_path + '/002.out'
    
    root = xml.etree.ElementTree.parse(statement_path).getroot()

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
