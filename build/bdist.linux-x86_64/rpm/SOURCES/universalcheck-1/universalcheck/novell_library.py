#!/usr/bin/env python

import logging
import subprocess
import shlex
import re
import sqlite3
from ConfigParser import ConfigParser


class Logs:
    def __init__(self, file_log):
        self.logger = None
        if None is self.logger:
            self.logger = logging.getLogger('universalcheck')
            self.hdlr = logging.FileHandler(file_log)
            # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
            # self.hdlr.setFormatter(formatter)
            self.logger.addHandler(self.hdlr)
            self.logger.setLevel(logging.DEBUG)

    def info_log(self, message):
        self.logger.info(message)
        self.logger.removeHandler(self.hdlr)


class Utilities:
    def __init__(self):
        pass

    @staticmethod
    def command(command):
        cmd = shlex.split(command)
        out = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        errout = out.stderr.read()
        sout = out.stdout.read()
        return sout, errout

    @staticmethod
    def command_optimize(command):
        cmd = shlex.split(command)
        out = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        outok = out.stdout.read()
        errout = out.stderr.read()
        return errout, outok

    @staticmethod
    def interface_info(neworkiface):
        command = 'ip addr sh ' + neworkiface
        cmd = shlex.split(command)
        out = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = out.communicate()
        if output[0] is not None:
            info = output[0]
            str(info).splitlines()
            for line in info:
                if re.search('inet', line) and not re.search('secondary', line):
                    ip_data = line.split(" ")[1].split("/")[0]
                    return ip_data
        else:
            pass

    @staticmethod
    def search_process_is_alive(process_name):
        command = "ps aux"
        cmd = shlex.split(command)
        out = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = out.communicate()

        cmd_system = output[0].splitlines()

        for process in cmd_system:
            if re.search(process_name, process):
                return 0
            else:
                return 1

    @staticmethod
    def configIni():
        file_config = "universalcheck.conf"
        config = ConfigParser()
        config.read(file_config)
        command_edir = config.get('comandoschek', 'edir')

        return command_edir,

