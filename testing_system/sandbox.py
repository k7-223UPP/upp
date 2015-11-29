import subprocess
import resource
from testing_system import verdict
from task_library import task_reader


def set_limits(memory_limit):
    resource.setrlimit(resource.RLIMIT_AS, memory_limit, memory_limit + 1)


def get_output(code_link, input_file_name, time_limit, memory_limit, test_number):
    with open(input_file_name, 'r') as input_file:
        process = subprocess.Popen(code_link, stdin=input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=set_limits(memory_limit))
        try:
            out, err = process.communicate(timeout=time_limit)
        except subprocess.TimeoutExpired:
            process.kill()
            raise verdict.TimeLimit(test_number)
        except MemoryError:
            process.kill()
            raise verdict.MemoryLimit(test_number)

        SUCCESSFUL_RETURN_CODE = 0
        if process.returncode != SUCCESSFUL_RETURN_CODE:
            raise verdict.RuntimeError(test_number)

        return out


def process_test(code_link, task_id, test_number):
    time_limit = float(task_reader.get_time_limit(task_id))

    MEGA = 1024 * 1024
    memory_limit = int(task_reader.get_memory_limit(task_id)) * MEGA

    input_file_name = task_reader.get_input_test_path(task_id, test_number)
    output_file_name = task_reader.get_output_test_path(task_id, test_number)

    output = get_output(code_link, input_file_name, time_limit, memory_limit, test_number)

    with open(output_file_name, 'w') as output_file:
        output_file.write(output)