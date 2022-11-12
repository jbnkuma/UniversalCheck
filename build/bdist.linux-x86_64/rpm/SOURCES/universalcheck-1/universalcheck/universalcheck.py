#!/usr/bin/env python2.6
import datetime

import novell_library


class UniversalCheck:
    def __init__(self):
        self.utilities = novell_library.Utilities()
        self.LAGS = ""

    def edir389(self):
        """
        check is alive
        """
        hostname = self.utilities.command("hostname")[0]
        file_to_log = "/var/log/availability/" + hostname.strip() + ".availability." + datetime.datetime.now().strftime(
            "%d-%m-%Y-%H")
        print file_to_log
        # command = self.utilities.configIni()[0]
        command = 'ldapsearch -LLL -x -h localhost -p 389 -D cn=nts_proxy,ou=servicios,o=sat -w 4gr33 -b cn=nts_proxy,ou=servicios,o=sat cn'
        print datetime.datetime.now().strftime("|%d-%m-%Y|%H:%M")
        output = self.utilities.command_optimize(command)
        print datetime.datetime.now().strftime("|%d-%m-%Y|%H:%M")
        if output[1].strip() == '':
            log = novell_library.Logs(file_to_log)
            log.info_log(hostname.strip() + datetime.datetime.now().strftime("|%d-%m-%Y|%H:%M|DOWN"))
        else:
            log = novell_library.Logs(file_to_log)
            log.info_log(hostname.strip() + datetime.datetime.now().strftime("|%d-%m-%Y|%H:%M|UP"))

    def lagherbeat(self):
        pass


test = UniversalCheck()
test.edir389()


