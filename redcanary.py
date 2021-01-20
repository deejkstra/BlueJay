#!/usr/bin/env python3

import os
import sys
import pwd
import json
import random
import string
import datetime
import socket
import threading
import queue

q = queue.Queue()

def random_string():
    return ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(64)])


def start_process(command):
    print('start_process', command)
    os.system(command)
    return {}


def create_file(filename):
    print('create_file', filename)
    with open(filename, "w+") as f:
        f.write(random_string())

    return {
        'filepath': filename,
        'operation': 'create'
    }


def edit_file(filename):
    print('edit_file', filename)
    with open(filename, "w") as f:
        f.write(random_string())

    return {
        'filepath': filename,
        'operation': 'edit'
    }


def delete_file(filename):
    print('delete_file', filename)
    os.remove(filename)

    return {
        'filepath': filename,
        'operation': 'delete'
    }


def server(port, payload, q):
    s = socket.socket()
    s.bind(('', port))
    s.listen(5)

    print('starting server')
    c, addr = s.accept()
    print('Got connection from', addr)
    c.send(payload.encode())
    c.close()
    q.put(addr)
    

def client(host, port):
    s = socket.socket()
    s.connect((host, port))
    payload = s.recv(1024).decode()
    print(payload)
    s.close()
    return payload

def start_network(port):
    print('start_network', port)
    port = int(port)

    t = threading.Thread(name='Server', target=server, args=[port, random_string(), q])
    t.start()

    payload = client('localhost', port)

    t.join()
    source_addr = q.get()

    return {
        'source': '%s:%d' % source_addr,
        'destination': 'localhost:%d'.format(port),
        'payload_size': len(payload),
        'protocol': 'tcp',
    }


def main(args):
    print('main')
    flag_map = {
        '--start-process': start_process,
        '--create-file': create_file,
        '--edit-file': edit_file,
        '--delete-file': delete_file,
        '--start-network': start_network,
    }

    def arg_to_data(arg):
        flag, value = arg.split('=', 1)
        return (flag[2:], value)

    try:
        if not args[1] in flag_map:
            raise Exception('Invalid flag.')

        param_data = dict([arg_to_data(arg) for arg in args[2:]])
        function_log_data = flag_map[args[1]](**param_data)

        log_filename = datetime.datetime.now().strftime("redcanary_%Y-%m-%d.json")
        with open(log_filename, 'a') as f:
            json.dump({
                'timestamp': str(datetime.datetime.now()),
                'username': pwd.getpwuid(os.getuid()).pw_name,
                'process_id': os.getpid(),
                'process_name': 'redcanary',
                'process_command': ' '.join(args),
                **function_log_data,
            }, f)
            f.write("\n")
    except Exception as e:
        print(e)


# Execution
main(sys.argv)
