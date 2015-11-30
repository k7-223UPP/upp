# -*- coding: utf-8 -*-

class Verdict(BaseException):
    def __str__(self):
        return '-------'

class Accepted(Verdict):
    def __str__(self):
        return 'AC'

class WrongAnswer(Verdict):
    def __init__(self, test_number):
        self.test_number = test_number

    def __str__(self):
        return 'WA ' + str(self.test_number)

class MemoryLimit(Verdict):
    def __init__(self, test_number):
        self.test_number = test_number

    def __str__(self):
        return 'ML ' + str(self.test_number)

class TimeLimit(Verdict):
    def __init__(self, test_number):
        self.test_number = test_number

    def __str__(self):
        return 'TL ' + str(self.test_number)

class RuntimeError(Verdict):
    def __init__(self, test_number):
        self.test_number = test_number

    def __str__(self):
        return 'RE ' + str(self.test_number)

class CompilationError(Verdict):
    def __str__(self):
        return 'CE'