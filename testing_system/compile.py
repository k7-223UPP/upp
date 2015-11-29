# -*- coding: utf-8 -*-

from testing_system import verdict
from upp import settings
import subprocess
import os

MAKE_SUCCESSFUL_STATUS = 0
MAKE_FILE_NAME = 'makefile'
SOURCES = 'sources'
CPP_EXTENSION = '.cpp'

def compile(id_submission):
    sources_path = settings.BASE_DIR + os.sep + SOURCES
    relative_code_path = str(id_submission) + CPP_EXTENSION
    make_status = subprocess.call(['make', '-C ' + sources_path, \
                                   '-f ' + MAKE_FILE_NAME, \
                                    relative_code_path])
    if make_status != MAKE_SUCCESSFUL_STATUS:
        raise verdict.CompilationError()
    absolute_build_path = sources_path + os.sep + str(id_submission)
    return absolute_build_path