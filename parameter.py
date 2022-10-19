from subprocess import run
import sys
import os

# Current path of the script
script_path = os.path.dirname(__file__)


def check_option(option_input: str, value_input: str):
    if option_input == '-b':
        execute_shell_script('backup_script.sh', '', value_input)
    elif option_input == '-bm':
        execute_shell_script('backup_script.sh', '', value_input)
    elif option_input == '-h':
        print('\n'
              'Description:\tA tool to back up single or multiple objects.\n'
              '\t\tImportant objects can be highlighted as jewels.\n'
              '\n'
              'Usage:\t\tpython backup.py -[OPTION] <VALUE(S)>\n'
              '\n'
              '-b <VALUE>\tBack up a single object\n'
              '\t\t-> Value must include the full path of the object\n'
              '-h\t\tDisplay the help page\n'
              '-j <VALUE>\tHighlight an object as a jewel\n'
              '-m <VALUES>\tAdd this option to other options to choose multiple objects\n'
              '-v\t\tViews all currently highlighted jewels'
              '\n')
    elif option_input == '-j':
        execute_shell_script('jewel_script.sh', '', value_input)
    elif option_input == '-jm':
        execute_shell_script('jewel_script.sh', '', value_input)
    elif option_input == '-m':
        print('Error: Try \'python backup.py -h\' for help')
    return


def execute_shell_script(script_name: str, script_option: str, value_input: str):
    if script_option == '':
        run(f'./{script_name} {value_input}', shell=True, cwd=script_path)
    else:
        run(f'./{script_name} {script_option} {value_input}', shell=True, cwd=script_path)


if __name__ == '__main__':
    option, value = '', ''
    try:
        option = str(sys.argv[1])
        value = str(sys.argv[2])
        check_option(option, value)
    except:
        if option == '-h' or '-j':
            check_option(option, '')
        elif option == '-m':
            print('Error: Try \'python backup.py -h\' for help')
        else:
            print('Error: Try \'python backup.py -h\' for help')
