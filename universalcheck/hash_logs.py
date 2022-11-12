#!/usr/bin/env python
import datetime
import os

import sys

try:
    import sqlite3
except:
    pass
# import pysqlite2

from novell_library import Utilities, Logs, DataBase

"""
    :author: Jesus Becerril Navarrete
    :organization: 
    :contact: jesusbn5@protonmail.com 

"""
__docformat__ = "restructuredtext"

log = Logs("/var/log/slamon/md5sum_sla.log")


class HashLogAvailability:
    def __init__(self, logger):
        self.utils = Utilities
        self.HEAD = "/var/log/availability/"
        self.BODY = ".availability."
        self.services = {"edir389": "edir", "lagherbeat": "lag", "lagherbeattmp": "lage", "idpheartbeat": "idp",
                         "tomcat_imanager": "imanager", "indexauth": "indexauth", "satcserv": "satcserv",
                         "satauth": "satauth", "ciecinte": "ciecinter", "ciecintra": "ciecintra",
                         "wsau": "wsau", "wsfe": "wsfe", "superlumin": "superlumin", "nagios": "nagios",
                         "nagios_noc": "nagios_noc", "server_uptime": "server_uptime"}
        self.log = logger

    def normalize_db(self, db_file):
        self.log.info_log("Iniciando la normalizacion de la bitacora %s " % db_file)
        try:
            if os.path.exists(db_file.strip()):
                connection = sqlite3.Connection(db_file.strip())
                cursor = connection.cursor()
                statement = """DELETE FROM  logbook WHERE Time IN
                              (
                               SELECT MIN(Time) AS [DeleteTime]
                               FROM logbook
                               GROUP BY  Time
                               HAVING COUNT(*) > 1 ORDER BY Time ASC
                              )"""
                cursor.execute(statement)
                cursor.close()
                connection.close()
                self.log.info_log("La bitacora %s  se a normalizado sin inconvenientes" % db_file)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    def normalize_file(self, logbook_file):
        try:
            self.log.info_log("Ordenando bitacora del cliente")
            if os.path.exists(logbook_file):
                command = "env sort -u  " + logbook_file
                lines = self.utils.command(command, self.log)
                log = open(logbook_file, "w")
                for line in lines:
                    log.write(line)
                self.log.info_log("El proceso de ordenamiento y escritura del archivo fue exitoso")
                log.close()
            else:
                self.log.error_log(
                    "El archivo %s no existe verifica que universalcheck este activo o si hay problemas de escritura en disco" % logbook_file)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))


    def normalize_logbook(self, file_log):
        self.log.info_log("Validando el servicio que se esta monitoreando")
        modules = self.utils.init_program(self.log)
        statements = "*"
        table = "logbook"
        provisory = "  ORDER BY Time ASC"

        if modules != None and modules != "":
            self.log.info_log("El servicio que se esta monitoreando es: %s" % modules)
            hostname = self.utils.command("hostname", self.log)[0]
            date_diff = datetime.datetime.now() - datetime.timedelta(hours=1)
            date_file = date_diff.strftime("%d-%m-%Y-%H")
            date_dir = datetime.datetime.now().strftime("%d%m%Y") + "/"
            file_to_log_db = self.HEAD + date_dir + hostname.strip() + self.BODY + self.services[
                modules.strip()] + "." + date_file + ".db"
            try:
                self.log.info_log("La bitacora de monitoreo es: %s" % file_to_log_db)
                if os.path.exists(file_to_log_db):
                    self.normalize_db(file_to_log_db)
                    db = DataBase(self.log, file_to_log_db)
                    result = db.dataSearch(statements, table, provisory, "")
                    tdb = db.total_data('Hostname', 'Logbook')
                    tdf = 0
                    if os.path.exists(file_log):
                        tmp = open(file_log, 'r')
                        lines_tmp = tmp.readlines()
                        tdf = len(lines_tmp)

                    if tdb > tdf:
                        self.log.info_log("Iniciando la escritura de la bitacora del cliente: %s" % file_log)
                        log = open(file_log, "w")
                        for i in result[0].fetchall():
                            data = i[1] + "|" + i[2] + "|" + i[3] + "|" + i[4] + "\n"
                            log.write(str(data))
                        log.close()
                        result[1].close()
                        self.log.info_log("La escritura de la bitacora del cliente: %s fue exitosa" % file_log)
                    else:
                        self.log.info_log("Intentando normalizado solo de la bitacora cliente")
                        self.normalize_file(file_log)
                else:
                    self.log.info_log("Intentando normalizado de emergencia")
                    self.normalize_file(file_log)
                    self.log.info_log("La escritura de la bitacora del cliente: %s fue exitosa" % file_log)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))
                self.log.info_log("Iniciando normalizado de emergencia sobre bitacora del cliente")
                self.normalize_file(file_log)

    def create_hash(self):
        hostname = self.utils.command("hostname", self.log)[0]
        date_diff = datetime.datetime.now() - datetime.timedelta(hours=1)
        date_file = date_diff.strftime("%Y%m%d-%H")
        file_to_log = self.HEAD + hostname.strip() + self.BODY + date_file
        self.log.info_log("Se inicia el proceso de escritura de la bitacora del cliente")
        self.normalize_logbook(file_to_log)
        self.log.info_log("Iniciando la generacion del md5 de la bitacora de SLA, archivo %s" % file_to_log)
        cmd = "/usr/bin/env md5sum " + file_to_log
        hash_sum = self.utils.command(cmd, self.log)[0]
        if hash_sum != None and hash_sum != "":
            self.log.info_log("El md5sum de la bitacora %s se genero sin problemas" % file_to_log)
            sum_file = file_to_log + ".txt"
            try:
                self.log.info_log(
                    "Iniciando la escritura del md5 de la bitacora del cliente en el archivo %s" % sum_file)
                file_md5sum = open(sum_file, "w")
                file_md5sum.write(hash_sum.split(" ")[0])
                self.log.info_log("Se ha escrito la bitacora del cliente en el archivo %s" % sum_file)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))
        else:
            self.log.error_log("Se produjo un error al generar el md5sum")


if __name__ == "__main__":
    hash_logbook = HashLogAvailability(log)
    hash_logbook.create_hash()
