#!/usr/bin/env python
import datetime
import sys

import os
import re

import novell_library

"""
    :author: Jesus Becerril Navarrete
    :organization: 
    :contact: jesusbn5@protonmail.com

"""
__docformat__ = "restructuredtext"

log = novell_library.Logs("/var/log/slamon/universalcheck.log")


class UniversalCheck:
    def __init__(self, logger):
        """
        Funcion que inicializa la clase es muy similar a un constructor se dan de alta las varialbles de clase utilities
        HEAD y BODY que son auxiliares en la creacion del nombre del archivo de las bitacoras.
        """
        self.utilities = novell_library.Utilities()
        self.HEAD = "/var/log/availability/"
        self.BODY = ".availability."
        self.log = logger

    def write_db_message(self, status, service, mytime):
        """
        Funcion  que realiza la incercion del dato de estado de cualquiera de las funciones de validacion de servicios.
        :param status: Variable que contiene el estado del servicio que se valida y el cual es escrito en el archivo .db
        que servira de bitacora.
        """
        try:
            log.info_log("Escribiendo en la bitacora el resultado")
            hostname = self.utilities.command("hostname", log)[0]
            TABLE = "  logbook "
            statements = ''' (Hostname, Date, Time, Status) '''
            provisory = ''' (?,?,?,?) '''
            date_dir = datetime.datetime.now().strftime("%d%m%Y") + "/"
            if os.path.exists(self.HEAD + date_dir):
                pass
            else:
                os.makedirs(self.HEAD + date_dir)
            date_file = datetime.datetime.now().strftime("%d-%m-%Y-%H")
            file_to_log_db = self.HEAD + date_dir + hostname.strip() + self.BODY + service + "." + date_file + ".db"
            db = novell_library.Create_Table(log, file_to_log_db)
            db.init_db(log)

            db_util = novell_library.DataBase(log, file_to_log_db)
            last_time = db_util.get_last_row(table=TABLE)
            if last_time != None:
                hour, minutes = last_time[3].split(":")
                last_db = datetime.timedelta(hours=int(hour), minutes=int(minutes))
                next_time = last_db + datetime.timedelta(minutes=1)
                hour1, minutes1 = mytime.split(":")
                last_in = datetime.timedelta(hours=int(hour1), minutes=int(minutes1))
                if last_in == last_db:
                    pass
                else:

                    if next_time != last_in:
                        target_hour, target_min = str(next_time).split(":")
                        if int(target_min) > 59 or int(target_hour) > int(hour1):
                            pass
                        else:
                            target_time = datetime.datetime.strptime(str(target_hour + ":" + target_min), "%H:%M")
                            data = hostname.strip(), datetime.datetime.now().strftime("%d-%m-%Y"), \
                                   target_time.strftime("%H:%M"), status
                            db_util.insertion(TABLE, statements, provisory, data)
                            self.write_log_message(status, service, target_time.strftime("%H:%M"))
                    else:
                        data = hostname.strip(), datetime.datetime.now().strftime("%d-%m-%Y"), \
                               mytime, status
                        db_util.insertion(TABLE, statements, provisory, data)
                        self.write_log_message(status, service, mytime)

            else:
                data = hostname.strip(), datetime.datetime.now().strftime("%d-%m-%Y"), \
                       mytime, status
                db_util.insertion(TABLE, statements, provisory, data)
                self.write_log_message(status, service, mytime)
        except:
            self.write_log_message(status, service, mytime)

    def write_log_message(self, status, service, mytime):
        """
        Funcion  que realiza la escritura del dato de estado de cualquiera de las funciones de validacion de servicios.
        :param status: Variable que contiene el estado del servicio que se valida y el cual es escrito en el archivo txt
        que servira de bitacora.
        """
        try:
            hostname = self.utilities.command("hostname", self.log)[0]
            date_file = datetime.datetime.now().strftime("%Y%m%d-%H")
            file_to_log = self.HEAD + hostname.strip() + self.BODY + date_file
            log = novell_library.LogsLogbook(file_to_log)
            file_tmp = open(file_to_log, 'r')
            aux = file_tmp.readlines()
            aux2 = ""
            for i in aux:
                aux2 = i
            try:
                last_time = aux2.strip().split("|")[2]
            except:
                last_time = None

            if last_time != None:
                hour, minutes = last_time.split(":")
                last_db = datetime.timedelta(hours=int(hour), minutes=int(minutes))
                next_time = last_db + datetime.timedelta(minutes=1)
                hour1, minutes1 = mytime.split(":")
                last_in = datetime.timedelta(hours=int(hour1), minutes=int(minutes1))
                if last_in == last_db:
                    pass
                else:
                    if next_time != last_in:
                        target_hour, target_min = str(next_time).split(":")
                        if int(target_min) > 59 or int(target_hour) > int(hour1):
                            pass
                        else:
                            try:
                                target_time = datetime.datetime.strptime(str(target_hour + ":" + target_min), "%H:%M")
                            except:
                                import time
                                t_aux = time.strptime(str(target_hour + ":" + target_min), "%H:%M")
                                target_time = datetime.datetime(*t_aux[:6])
                            message = hostname.strip() + datetime.datetime.now().strftime(
                                "|%d-%m-%Y|") + target_time.strftime("%H:%M") + "|" + status
                            log.info_log(message)
                            self.log.info_log(message)
                            self.log.info_log("La informacion fue escrita sin inconvenientes")
                    else:
                        message = hostname.strip() + datetime.datetime.now().strftime(
                            "|%d-%m-%Y|") + mytime + "|" + status
                        log.info_log(message)
                        self.log.info_log(message)
                        self.log.info_log("La informacion fue escrita sin inconvenientes")

            else:
                message = hostname.strip() + datetime.datetime.now().strftime("|%d-%m-%Y|" + mytime + "|" + status)
                log.info_log(message)
                self.log.info_log(message)
                self.log.info_log("La informacion fue escrita sin inconvenientes")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.log.error_log("Se presento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    def validate_curl(self, output, service, ftime):
        """
        Funcion  que valida la respuesta de los servicios validados por una peticion http y escribe el estado en la
        bitacora sqlite.
        :param output: Variable que contiene la salida del comando curl y la peticion http realizada.
        """
        if re.search('200,', output[0]) or re.search('000', output[0]):
            self.write_db_message("UP", service, ftime)
        else:
            self.write_db_message("DOWN", service, ftime)

    def validate_curl_(self, output):
        """
        Funcion  que valida la respuesta de los servicios validados por una peticion http y escribe el estado en la
        bitacora sqlite.
        :param output: Variable que contiene la salida del comando curl y la peticion http realizada.
        """
        if re.search('200,', output[0] or re.search('000', output[0])):
            return "UP"
        else:
            return "DOWN"

    def validate_alive(self, output, service):
        """
        Funcion  que escribe el estado de un procesos buscado, dependiendo de si el estado esta activo o inactivo.
        :param output: Variable que contiene el estado del servicio que se valida y el cual es escrito en el archivo .db
        que servira de bitacora.
        """
        if output:
            self.write_db_message("UP", service, datetime.datetime.now().strftime("%H:%M"))
        else:
            self.write_db_message("DOWN", service, datetime.datetime.now().strftime("%H:%M"))

    def edir389(self):
        """
        Funcion que valida si el sevicio eDirectory esta activo
        """
        self.log.info_log("Validando el servicio de eDirectory")
        command = self.utilities.configIni(log)[0]
        self.log.info_log("Ejecutando  el comando: %s" % command)
        output = self.utilities.command(command, log)
        self.log.info_log("Se ha ejecutado el comando, procediendo a la validacion del resultado del comando")
        if output[0] != None:
            if (re.search('cn=sla_proxy', output[0])) or (re.search('cn: sla_proxy', output[0])):
                self.write_db_message("UP", "edir", datetime.datetime.now().strftime("%H:%M"))
            else:
                self.write_db_message("DOWN", "edir", datetime.datetime.now().strftime("%H:%M"))
        else:
            self.write_db_message("DOWN", "edir", datetime.datetime.now().strftime("%H:%M"))

    def lagherbeat(self):
        """
        Funcion que valida de los servidores LAGs que el servicio se encuentra activo, realiza una busqueda en una
        base de datos de los servidores LAGs y el servidor donde esta ejecutando la tarea, realiza la preticion y
        escribe el estatus.
        """
        self.log.info_log("Iniciando la validacion de los servicios LAGs")
        hostname = self.utilities.command("hostname", log)[0]
        self.log.info_log(
            "Obteniendo los datos del servidor LAGs de la base:")
        file_json = novell_library.Utilities().json_info(self.log)
        data = novell_library.Utilities.read_json(file_json, hostname.strip())
        Ip = data[0]
        Port = data[1]

        if Ip != None and Port != None:
            try:
                rtime = datetime.datetime.now().strftime("%H:%M")

                url = Ip + ":" + Port
                command = str(self.utilities.configIni(self.log)[1]).encode(
                    'utf-8') + "  -k https://%s/nesp/app/heartbeat" % url
                result_command = self.utilities.command(command.encode('utf-8'), self.log)
                self.validate_curl(result_command, "lag", rtime)

            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.log.error_log("Se presento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    def lagherbeattmp(self):
        """
        Funcion que valida de los servidores LAGE se encuentre activo el servico, realiza una busqueda en una base
        de datos de los servidores LAGE y el servidor donde esta ejecutando la tarea, realiza la preticion y escribe
        el estatus.
        """
        hostname = self.utilities.command("hostname", self.log)[0]
        file_json = novell_library.Utilities().json_info(self.log)
        data = novell_library.Utilities.read_json(file_json, hostname.strip())
        Ip = data[0]
        Port = data[1]

        if Ip != None and Port != None:
            try:
                data = hostname.strip(),
                rtime = datetime.datetime.now().strftime("%H:%M")
                url = Ip + ":" + Port
                command = str(self.utilities.configIni(self.log)[1]).encode(
                    'utf-8') + "  http://%s/nesp/app/heartbeat" % url
                result_command = self.utilities.command(str(command).encode('utf-8'), self.log)
                self.validate_curl(result_command, "lage", rtime)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.log.error_log("Se presento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    def idpheartbeat(self):
        """
        Funcion que valida el servicio IDP, realiza la peticion y escribe el estatus.
        """
        rtime = datetime.datetime.now().strftime("%H:%M")
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[1] + "  -k https://%s:8443/nidp/idff/heartbeat" % niface
        result_command = self.utilities.command(command, self.log)
        self.validate_curl(result_command, "idp", rtime)

    def tomcat_imanager(self):
        """
        Funcion que valida el servicio tomcat de las consolas  se encuentra activo, realiza la peticion
        y escribe el estatus.
        """
        self.log.info_log("Buscando el proceso del tomcat")
        output = self.utilities.search_process_is_alive("tomcat", self.log)
        self.log.info_log("Validando si la consola iManager esta activa")
        self.validate_alive(output, "")

    def indexauth(self):
        """
        Funcion que valida los servicios.
        """
        cserv_out = self.satauth_()
        auth_out = self.satcserv_()
        rtime = datetime.datetime.now().strftime("%H:%M")
        self.write_db_message(cserv_out, "indexauth", rtime)
        self.write_db_message(auth_out, "indexauth", rtime)

    def satcserv_(self):
        """
        Funcion que valida el servicio mendiante una peticion con el comando curl y escribe el estatus de la respuesta
        del servicio.
        """
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[
                      2] + "  http://%s:" % niface
        result_command = self.utilities.command(command, self.log)
        out_satcserv = self.validate_curl_(result_command)
        return out_satcserv

    def satcserv(self):
        """
        Funcion que valida el servicio mendiante una peticion con el comando curl y escribe el estatus de la respuesta
        del servicio.
        """
        rtime = datetime.datetime.now().strftime("%H:%M")
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[
                      2] + "  http://%s:" % niface
        result_command = self.utilities.command(command, self.log)
        self.validate_curl(result_command, "", rtime)

    def satauth_(self):
        """
        Funcion que valida el servicio   mendiante una peticion con el comando curl y escribe el
        estatus de la respuesta del servicio.
        """
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[
                      2] + "  http://%s:" % niface
        result_command = self.utilities.command(command, self.log)
        out_satauth = self.validate_curl_(result_command)
        return out_satauth

    def satauth(self):
        """
        Funcion que valida el servicio SATAuthenticator  mendiante una peticion con el comando curl y escribe el
        estatus de la respuesta del servicio.
        """
        rtime = datetime.datetime.now().strftime("%H:%M")
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[
                      2] + "  http://%s:" % niface
        result_command = self.utilities.command(command, self.log)
        self.validate_curl(result_command, "satauth", rtime)

    def indexciec(self):
        """
        Funcion que valida los servicios ciecinter y el servicio ciecintra.
        """
        out_ciecinter = self.ciecinter_()
        out_ciecintra = self.ciecintra_()
        rtime = datetime.datetime.now().strftime("%H:%M")
        self.write_db_message(out_ciecinter, "indexciec", rtime)
        self.write_db_message(out_ciecintra, "indexciec", rtime)

    def ciecinter_(self):
        """
        Funcion que valida el servicio  mendiante una peticion con el comando curl y escribe el
        estatus de la respuesta del servicio.
        """
        rtime = datetime.datetime.now().strftime("%H:%M")
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[2] + "  http://%s:8080" % niface
        result_command = self.utilities.command(command, self.log)
        result_ciecinter = self.validate_curl_(result_command)
        return result_ciecinter

    def ciecinter(self):
        """
        Funcion que valida el servicio  mendiante una peticion con el comando curl y escribe el
        estatus de la respuesta del servicio.
        """
        rtime = datetime.datetime.now().strftime("%H:%M")
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[2] + "  http://%s" % niface
        result_command = self.utilities.command(command, self.log)
        self.validate_curl(result_command, "ciecinter", rtime)

    def ciecintra_(self):
        """
        Funcion que valida el servicio  mendiante una peticion con el comando curl y escribe el
        estatus de la respuesta del servicio.
        """
        rtime = datetime.datetime.now().strftime("%H:%M")
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[2] + "  http://%s:" % niface
        result_command = self.utilities.command(command, self.log)
        result_ciecintra = self.validate_curl_(result_command)
        return result_ciecintra

    def ciecintra(self):
        """
        Funcion que valida el servicio  mendiante una peticion con el comando curl y escribe el
        estatus de la respuesta del servicio.
        """
        rtime = datetime.datetime.now().strftime("%H:%M")
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[2] + "  http://%s:" % niface
        result_command = self.utilities.command(command, self.log)
        self.validate_curl(result_command, "ciecintra", rtime)

    def wsau(self):
        """
        Funcion que valida el servicio   mendiante una peticion con el comando curl y escribe el
        estatus de la respuesta del servicio.
        """
        rtime = datetime.datetime.now().strftime("%H:%M")
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[2] + "  http://%s:80/WSIdentity/WSAA?wsdl" % niface
        result_command = self.utilities.command(command, self.log)
        self.validate_curl(result_command, "wsau", rtime)

    def wsfe(self):
        """
        Funcion que valida el servicio mendiante una peticion con el comando curl y escribe el
        estatus de la respuesta del servicio.
        """
        rtime = datetime.datetime.now().strftime("%H:%M")
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[2] + "  http://%s:" % niface
        result_command = self.utilities.command(command, self.log)
        self.validate_curl(result_command, "wsfe", rtime)

    def superlumin(self):
        """
        Funcion que valida el servicio   mendiante una peticion con el comando netcat y escribe el
        estatus de la respuesta del servicio.
        """
        niface = self.utilities.interface_info(self.utilities.netiface(self.log), self.log)
        command = self.utilities.configIni(self.log)[3] + "  " + niface + "  " + str(8080)
        output = self.utilities.command(command, self.log)
        if re.search('open', output[1]):
            self.write_db_message("UP", "superlumin", datetime.datetime.now().strftime("%H:%M"))
        else:
            self.write_db_message("DOWN", "superlumin", datetime.datetime.now().strftime("%H:%M"))

    def nagios(self):
        """
        Funcion que valida el servicio Nagios (Agente) se encuentre activo y escribe el estatus de este en la bitacora.
        """
        output = self.utilities.search_process_is_alive("/usr/sbin/nagios -d /etc/nagios/nagios.cfg", self.log)
        self.validate_alive(output, "nagios")

    def nagios_noc(self):
        """
        Funcion que valida el servicio Nagios en el servidor central se encuentre activo y escribe el estatus de este
        en la bitacora.
        """
        output = self.utilities.search_process_is_alive("", self.log)
        self.validate_alive(output, "")

    def server_uptime(self):
        """
        Funcion que valida que se encuentre activo el servidor anotando este dato en el la bitacora.
        """
        output = self.utilities.command("uptime", self.log)
        if re.search('up', output[0]):
            self.write_db_message("UP", "server_uptime", datetime.datetime.now().strftime("%H:%M"))
        else:
            self.write_db_message("DOWN", "server_uptime", datetime.datetime.now().strftime("%H:%M"))

    def app_run(self, module):
        """
        Funcion axuliar para inicializar la aplicacion, siendo esta un case para iniciar la funcion de monitoreo del
        servicio encontradon en el archivo de configuracion.
        """
        log.info_log("Iniciando la validacion de el servicio: %s" % module)
        if module == 'edir389':
            self.edir389()
        elif module == 'lagherbeat':
            self.lagherbeat()
        elif module == 'lagherbeattmp':
            self.lagherbeattmp()
        elif module == 'idpheartbeat':
            self.idpheartbeat()
        elif module == 'tomcat_imanager':
            self.tomcat_imanager()
        elif module == 'indexauth':
            self.indexauth()
        elif module == '':
            self.satcserv()
        elif module == '':
            self.satauth()
        elif module == '':
            self.indexciec()
        elif module == '':
            self.ciecinter()
        elif module == '':
            self.ciecintra()
        elif module == 'wsau':
            self.wsau()
        elif module == 'wsfe':
            self.wsfe()
        elif module == 'superlumin':
            self.superlumin()
        elif module == 'nagios':
            self.nagios()
        elif module == 'nagios_noc':
            self.nagios_noc()
        elif module == 'server_uptime':
            self.server_uptime()


if __name__ == "__main__":
    module = novell_library.Utilities.init_program(log)
    if module != None and module != "":
        UniversalCheck(log).app_run(module)
