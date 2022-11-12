#!/usr/bin/env python
import sys

import re
from novell_library import Utilities, Logs


class LagConfig:
    def __init__(self):
        self.log = Logs("/tmp/lag_autoconfig.log")
        self.utils = Utilities()

    def validate_curl(self, output, ):
        """
        Funcion  que valida la respuesta de los servicios validados por una peticion http y escribe el estado en la
        bitacora sqlite.
        :param output: Variable que contiene la salida del comando curl y la peticion http realizada.
        """
        if re.search('200,', output[0]):
            return True

    def lagherbeat(self, Ip, Port):
        """
        Funcion que valida de los servidores LAGs que el servicio se encuentra activo, realiza una busqueda en una
        base de datos de los servidores LAGs y el servidor donde esta ejecutando la tarea, realiza la preticion y
        escribe el estatus.
        """
        self.log.info_log("Iniciando la validacion de los servicios LAGs")
        if Ip != None and Port != None:
            try:
                url = Ip + ":" + Port
                command = str(self.utils.configIni(self.log)[1]).encode(
                    'utf-8') + "  -k https://%s/nesp/app/heartbeat" % url
                result_command = self.utils.command(command.encode('utf-8'), self.log)
                return self.validate_curl(result_command)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.log.error_log("Se presento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    def lagherbeattmp(self, Ip, Port):
        """
        Funcion que valida de los servidores LAGE se encuentre activo el servico, realiza una busqueda en una base
        de datos de los servidores LAGE y el servidor donde esta ejecutando la tarea, realiza la preticion y escribe
        el estatus.
        """

        if Ip != None and Port != None:
            try:
                url = Ip + ":" + Port
                command = str(self.utils.configIni(self.log)[1]).encode(
                    'utf-8') + "  http://%s/nesp/app/heartbeat" % url
                result_command = self.utils.command(str(command).encode('utf-8'), self.log)
                return self.validate_curl(result_command)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.log.error_log("Se presento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    def eth1_info(self):

        """
        Funcion que obtiene la ip de la interfaz de red.
        :param networkiface: Variable que contiene la tarejeta de red con la que se realizara el proceso de obtencion
        de la ip
        :returns:ip_data: Valor de la ip obtenida
        """
        try:
            print ("Buscando ip del servidor")
            ip_list = []
            command = 'ip addr sh ' + "eth1"
            output = self.utils.command(command, self.log)
            info = str(output[0].decode("utf8")).splitlines()
            if len(info) > 0:
                for line in info:
                    if re.search('inet', line) and not re.search('inet6', line) and not re.search(
                            "BROADCAST,MULTICAST,UP,LOWER_UP", line):
                        ip_data = line.split("/")[0].split("inet")
                        if len(ip_data) > 1:
                            ip_list.append(ip_data[1].strip())
            return ip_list
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print ("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    def check_config(self, ip_list):
        for ip in ip_list:
            if self.lagherbeat(ip, "443"):
                print "La respuesta del la ip: %s por el puerto: %s fue satisfactoria procediendo a la configuracion" % (
                    ip, "443")
                hostname = self.utils.command("hostname", self.log)[0]
                hostname = hostname.replace('\n', '')
                file_json = self.utils.json_info(self.log)
                data_json = self.utils.read_json(file_json, hostname)

                if data_json[0] != None and data_json[1] != None:
                    print "Este lag ya esta configurado."
                    sys.exit(0)
                else:
                    print "Configurando los datos de este lag"
                    dict_data = {
                        hostname.strip('\n'): {"ip": ip,
                                               "port": "443"}
                    }
                    print dict_data
                    self.utils.write_json(file_json, dict_data)
                    sys.exit(1)

            elif self.lagherbeattmp(ip, "80"):
                print "La respuesta del la ip: %s por el puerto: %s fue satisfactoria procediendo a la configuracion" % (
                    ip, "80")
                hostname = self.utils.command("hostname", self.log)[0]
                file_json = self.utils.json_info(self.log)
                data_json = self.utils.read_json(file_json, hostname)

                if data_json[0] != None and data_json[1] != None:
                    print "Este lag ya esta configurado."
                    sys.exit(0)
                else:
                    print "Configurando los datos de este lag"
                    dict_data = {
                        hostname.strip('\n'): {"ip": ip,
                                               "port": "80"}
                    }
                    print dict_data
                    self.utils.write_json(file_json, dict_data)
                    sys.exit(2)

        print "Este servidor no es un servidor lag"
        sys.exit(3)

    def check_sh(self, sh_file):
        if sh_file != None:
            for line in sh_file[0].splitlines():
                if re.search("/usr/local/bin/universalcheck", line) and re.search("lag", line):
                    return True
        else:
            return False

    def config_run(self):
        command = "crontab -l"
        out = self.utils.command(command, self.log)
        print "Verificando la existencia del archivo universalcheck.sh"
        if self.check_sh(out):
            print "Este es un servidor  lag"
            ip_list = self.eth1_info()
            self.check_config(ip_list)
        else:
            print "El archivo universalcheck.sh no existe se verificara si este es servidor es un lag"
            ip_list = self.eth1_info()
            self.check_config(ip_list)


lag = LagConfig()
lag.config_run()
