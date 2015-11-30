# -*- coding: utf-8 -*-

from testing_system import verdict
import subprocess
import os
from task_library import task_reader

MAKE_SUCCESSFUL_STATUS = 0
MAKE_FILE_NAME = 'makefile'
SOURCES = 'sources'
CPP_EXTENSION = '.cpp'
CHECKER = 'checker'
CHECKER_SUCCESSFUL_STATUS = 0

def compile(id_submission, base_path):
    sources_path = base_path + os.sep + SOURCES
    absolute_code_path = sources_path + os.sep + relative_code_path
    absolute_make_file_path = sources_path + os.sep + MAKE_FILE_NAME
    make_status = subprocess.call(['make', \
                                   '-f', \
                                   absolute_make_file_path, \
                                   absolute_code_path])
    if make_status != MAKE_SUCCESSFUL_STATUS:
        raise verdict.CompilationError()
    absolute_build_path = sources_path + os.sep + str(id_submission)
    return absolute_build_path


def compare_outputs(id_task, input_file_name, output_file_name, \
                    user_output_file_name, test_number):
    checker_path = task_reader.get_checker_path(id_task)
    checker_status = subprocess.call(['source ', checker_path, \
                                      input_file_name, output_file_name, \
                                      user_output_file_name])
    if checker_status != CHECKER_SUCCESSFUL_STATUS:
        raise verdict.WrongAnswer(test_number)