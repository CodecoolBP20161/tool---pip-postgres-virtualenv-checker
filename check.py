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
    postgres_version = check_package_version('postgresql')
    if postgres_version is None:
        print('postgresql package is not installed! Install it with "sudo apt install postgresql postgresql-contrib"')
    else:
        print('postgresql ' + postgres_version + ' installed')
        postgres_contrib_version = check_package_version('postgresql-contrib')
        if postgres_contrib_version is None:
            print('postgresql-contrib package is not installed! Install it with "sudo apt install postgresql-contrib"')
        else:
            print('postgresql-contrib ' + postgres_contrib_version + ' installed')
            if postgres_version != postgres_contrib_version:
                print('postgresql and postgresql-contrib versions not match! Please update them!')


main()
