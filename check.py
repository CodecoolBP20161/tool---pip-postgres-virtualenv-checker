#!/usr/bin/python3
import subprocess


def run(command_list):
    process = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = process.stderr.decode("utf-8")  # returning the stderr text, if any
    if len(error) > 0:
        return error
    return process.stdout.decode("utf-8")


def check_package_version(package):
    stdout = run(['dpkg-query', '-W', '-f="${Version}"', package])
    if 'no packages found' in stdout:
        return None
    return stdout


def main():
    problem = False

    current_user = run(['whoami']).replace('\n', '')
    if current_user == 'root':
        print('Please run this script with your own user and without "sudo"! [ERRNO:1]')
        exit(1)

    postgres_version = check_package_version('postgresql')
    if postgres_version is None:
        problem = True
        print(
            ' - postgresql package is not missing! Install it with "sudo apt install postgresql postgresql-contrib"' +
            ' [ERRNO:2]')
    else:
        postgres_contrib_version = check_package_version('postgresql-contrib')
        if postgres_contrib_version is None:
            problem = True
            print(
                ' - postgresql-contrib package is not missing! ' +
                'Install it with "sudo apt install postgresql-contrib" [ERRNO:3]')
        else:
            if postgres_version != postgres_contrib_version:
                problem = True
                print(' - postgresql and postgresql-contrib versions not match! Please update them! [ERRNO:4]')

    is_postgres_user_exist = 'postgres' in run(['cut', '-d:', '-f1', '/etc/passwd'])
    if not is_postgres_user_exist:
        problem = True
        print(' - postgres user does not exist! [ERRNO:5]')

    if 'psql' not in run(['which', 'psql']):
        problem = True
        print(' - psql command is not found! [ERRNO:6]')

    psql_stdout = run(['psql'])
    # print(subprocess.run(['psql'], stdout=subprocess.PIPE))
    if 'role' in psql_stdout:
        problem = True
        print(' - Postgres DB can not find a database called "' + current_user + '", please create it! [ERRNO:7]')

    if run(['psql', '-tAc', 'SELECT 1 FROM pg_database WHERE datname=\'' + current_user + '\'']).strip() != '1':
        problem = True
        print(' - Postgres DB can not find a database called "' + current_user + '", please create it! [ERRNO:8]')
    #
    # Ending
    #

    if problem:
        print('\nThe test found the above problems, please fix them!')
        exit(1)
    else:
        print('postgresql ' + postgres_version + ' installed')
        print('postgresql-contrib ' + postgres_contrib_version + ' installed')
        print('Test ran successfully! Everything is OK!')

main()
