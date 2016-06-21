#!/usr/bin/python3
import subprocess


def run(command_list):
    return subprocess.run(command_list, stdout=subprocess.PIPE).stdout.decode("utf-8")


def check_package_version(package):
    stdout = run(['dpkg-query', '-W', '-f="${Version}"', package])
    if 'no packages found' in stdout:
        return None
    return stdout


def main():
    problem = False

    postgres_version = check_package_version('postgresql')
    if postgres_version is None:
        problem = True
        print(' - postgresql package is not missing! Install it with "sudo apt install postgresql postgresql-contrib"')
    else:
        postgres_contrib_version = check_package_version('postgresql-contrib')
        if postgres_contrib_version is None:
            problem = True
            print(' - postgresql-contrib package is not missing! Install it with "sudo apt install postgresql-contrib"')
        else:
            if postgres_version != postgres_contrib_version:
                problem = True
                print(' - postgresql and postgresql-contrib versions not match! Please update them!')

    is_postgres_user_exist = 'postgres' in run(['cut', '-d:', '-f1', '/etc/passwd'])
    if not is_postgres_user_exist:
        problem = True
        print(' - postgres user does not exist!')

    if 'psql' not in run(['which', 'psql']):
        problem = True
        print(' - psql command is not found!')

    if problem:
        print('The test found the above problems, please fix them!')
        exit(1)
    else:
        print('postgresql ' + postgres_version + ' installed')
        print('postgresql-contrib ' + postgres_contrib_version + ' installed')
        print('Test ran successfully! Everything is OK!')

main()
