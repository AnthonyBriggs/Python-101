#!/usr/bin/python

import os
import re


def log_files(dir_name, file_type):
    if not os.path.exists(dir_name):
        raise ValueError(dir_name + " not found!")    
    if not os.path.isdir(dir_name):
        raise ValueError(dir_name + " is not a directory!")

    for path, dirs, files in os.walk(dir_name):
        # print path
        # print dirs
        log_files = [f for f in files
                     if f.endswith(file_type)]
        for each_file in log_files:
            yield os.path.join(path, each_file)
        # print '-' * 42


def log_lines(dir_name, file_type):
    """
    # yield version:
    for each_file in log_files(dir_name, file_type):
        for each_line in file(each_file).readlines():
                yield each_line.strip()
    """
    return ((each_file, each_line.strip())
            for each_line in file(each_file).readlines()
            for each_file in log_files(dir_name, file_type))

def list_errors(dir_name, file_type):
    return (each_file + ': ' + each_line.strip()
            for each_file, each_line in log_lines(dir_name, file_type)
            if 'error' in each_line.lower())

apache_log_headers = ['host', 'client_id', 'user_id',
    'datetime', 'method', 'request', 'http_proto', 
    'status', 'size', 'referrer', 'user_agent']
logpats = (r'(\S+) (\S+) (\S+) \[(.*?)\] '
           r'"(\S+) (\S+) (\S+)" (\S+) (\S+) '
           r'"(.+)" "(.+)"')
logpat = re.compile(logpats)

def parse_apache(line):
    log_split = logpat.match(line)
    if not log_split:
        print("Line didn't match!")
        print(line)
        print()
        return None
        
    log_split = log_split.groups()
    result = dict(list(zip(apache_log_headers, log_split)))
    result['status'] = int(result['status'])
    if result['size'].isdigit():
        result['size'] = int(result['size'])
    else:
        result['size'] = 0
    return result
    
def apache_lines(dir_name, file_type):
    return (parse_apache(each_line) 
            for each_file, each_line in log_lines(dir_name, file_type))

if __name__ == '__main__':
    dir_name = '/var/log'
    file_type = '.log'

    if 0:
        for each_file in log_files(dir_name, file_type):
            print(each_file)
        print()

        for each_error in list_errors(dir_name, file_type):
            print(each_error)
        print('=' * 42)
        
    for each_file in log_files('/var/log/apache2', '.log'):
        print(each_file)
    print('-' * 42)
    
    if 1:
        for each_file, each_line in log_lines('/var/log/apache2', '.log'):
            print(each_file+":", each_line)
            print(parse_apache(each_line))
            print()
        
    print(sum((each_line['size']
        for each_line in apache_lines('/var/log/apache2', '.log')
        if each_line is not None and 'size' in each_line)))

