#!/usr/bin/env python
import logging
import shlex
import subprocess
import sys

import os
import re

"""
    :author: Jesus Becerril Navarrete
    :organization: 
    :contact: jesusbn5@protonmail.com

"""

__docformat__ = "restructuredtext"
# Validacion para importar el objeto ConfigParser en python3 y versiones menores a esta.
try:
    # Python < 3
    from ConfigParser import ConfigParser
except ImportError:
    # Python => 3
    from configparser import ConfigParser

try:
    import sqlite3
except ImportError:
    pass
# from pysqlite2 import dbapi2 as sqlite3
try:
    from hashlib import md5
except:
    import md5
class Logs:
    '''Clase destinada a los objetos que manipulan los archivos de texto o logs de esta aplicacion'''

    def __init__(self, file_log):
        """
        Funcion que inicializa la clase es muy similar a un constructor da de alta los objetos de clase logger para
        poder usarlos para escribir los mensajes en los archivos de log
        :param file_log: Archivo donde se escriran los mensajes de log.
        """
        self.logger = None
        if None is self.logger:
            self.logger = logging.getLogger('universalcheck')
            self.hdlr = logging.FileHandler(file_log)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
            self.hdlr.setFormatter(formatter)
            self.logger.addHandler(self.hdlr)
            self.logger.setLevel(logging.DEBUG)

    def info_log(self, message):
        """
        Funcion usada para crear el log con el nivel de prioridades de nivel 6  o mensajes informativos
        :param message: string que contiene el mensaje a escribir en el log
        """
        self.logger.info(message)

    #        self.logger.removeHandler(self.hdlr)

    def error_log(self, message):
        """
        Funcion usada para crear el log con el nivel de prioridades de nivel 3  o mensajes de error
        :param message: string que contiene el mensaje a escribir en el log
        """
        self.logger.error(message)


# self.logger.removeHandler(self.hdlr)

class LogsLogbook:
    '''Clase destinada a los objetos que manipulan los archivos de texto o logs de esta aplicacion'''

    def __init__(self, file_log):
        """
        Funcion que inicializa la clase es muy similar a un constructor da de alta los objetos de clase logger para
        poder usarlos para escribir los mensajes en los archivos de log
        :param file_log: Archivo donde se escriran los mensajes de log.
        """
        self.logger = None
        if None is self.logger:
            self.logger = logging.getLogger('universal')
            self.hdlr = logging.FileHandler(file_log)
            self.logger.addHandler(self.hdlr)
            self.logger.setLevel(logging.DEBUG)

    def info_log(self, message):
        """
        Funcion usada para crear el log con el nivel de prioridades de nivel 6  o mensajes informativos
        :param message: string que contiene el mensaje a escribir en el log
        """
        self.logger.info(message)
        self.logger.removeHandler(self.hdlr)


class Utilities:
    '''Clase que contiene las  funciones que se utilizan en el universal check de manera abstracta'''

    def __init__(self):
        """
        Funcion similar a un construcctor que inicializa la clase.
        """
        pass

    @staticmethod
    def command(command, log):
        """
        Funcion que realiza la ejecucion  de un comando tipo unix, esta funcion ejecuta el comando y lee la salida
        estandar asi como la salida de error y devuelve los valores leidos en cada salida.
        :param command: Variable que tiene el comando a ejexutar por la funcion.
        :returns:sout, errout: Devuelve los valores obtenidos  de las salidas de error y salida estandar del comando
        ejecutado.
        """
        try:
            log.info_log("Ejecutando el comando: %s " % command)
            cmd = shlex.split(command)
            out = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            sout, errout = out.communicate()
            return str(sout.decode("utf8")), str(errout.decode("utf8"))
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    @staticmethod
    def command_optimize(command, log):
        """
        Funcion que realiza la ejecucion  de un comando tipo unix, esta funcion ejecuta el comando y lee la salida
        estandar asi como la salida de error y devuelve los valores leidos en cada salida.
        :param command: Variable que tiene el comando a ejexutar por la funcion.
        :returns:sout, errout: Devuelve los valores obtenidos  de las salidas de error y salida estandar del comando
        ejecutado.
        """
        try:
            log.info_log("Ejecutando el comando: %s " % command)
            cmd = shlex.split(command)
            out = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            outok = out.stdout.read()
            errout = out.stderr.read()
            return errout, outok
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    @staticmethod
    def interface_info(neworkiface, log):
        """
        Funcion que obtiene la ip de la interfaz de red.
        :param log: Objeto para la escritura de logs
        :param neworkiface:  Variable que contiene la tarejeta de red con la que se realizara el proceso de obtencion
        de la ip
        :returns:ip_data: Valor de la ip obtenida
        """
        try:
            log.info_log("Buscando ip del servidor")
            command = 'ip addr sh ' + neworkiface
            cmd = shlex.split(command)
            out = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = out.communicate()
            info = str(output[0].decode("utf8")).splitlines()
            if len(info) > 0:
                for line in info:
                    if re.search('inet', line) and not re.search('secondary', line) and not re.search('inet6', line):
                        ip_data = line.split(" ")[5].split("/")[0]
                        return ip_data
            else:
                pass
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    @staticmethod
    def search_process_is_alive(process_name, log):
        """
        Funcion  que realiza una busqueda del proceso dado y revisa si existe en  ejecucion dicho comando.
        :param log:
        :param process_name: Proceso que se validara que este en ejecucion.
        :returns:Bool: Devuelve un valor bool True si encuentra el proceso dado activo si no lo encuentra devuelve
        el valor False.
        """
        try:
            log.info_log("Buscando el proceso %s en los procesos activos" % process_name)
            command = "ps aux"
            cmd = shlex.split(command)
            out = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = out.communicate()

            cmd_system = output[0].decode("utf8").splitlines()
            for process in range(len(cmd_system)):
                if re.search(process_name, cmd_system[process]):
                    return True
                else:
                    pass
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    @staticmethod
    def configIni(log):
        """
        Funcion de lectura de los parametros de configuracion de la aplicacion en un archivo de texo, lee los
        comandos que deberan usarse en las funciones de validacion de los servicios.
        :param log:
        :returns: command_edir, lag_command, csatc8080_command, cSuperLumin_command
        """
        try:
            file_config = "/etc/universalcheck/universalcheck.conf"
            config = ConfigParser()
            config.read(file_config)
            command_edir = config.get('comandoschek', 'edir')
            lag_command = config.get('comandoschek', 'clagheartbeat')
            csatc8080_command = config.get('comandoschek', 'csatc8080')
            cSuperLumin_command = config.get('comandoschek', 'cSuperLumin')
            return (command_edir, lag_command, csatc8080_command, cSuperLumin_command)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    @staticmethod
    def database_info(log):
        """
        Funcion que lee el dato de ubicacion del archivo con los datos de los servidores LAG  y LAGE
        :param log:
        :returns: file_db: Devuelve el directorio y el nobre completo del archivo con informacion de los servidores LAG
        y LAGE.
        """
        try:
            file_config = "/etc/universalcheck/universalcheck.conf"
            config = ConfigParser()
            config.read(file_config)
            file_db = config.get('dbconf', 'dbfile')
            return file_db
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    @staticmethod
    def netiface(log):
        """
        Funcion que devuelve la intefaz con la que estara trabajando la aplicacion la cual esta configurada en el
        archivo de texto plano usado para las configuracione.
        :param log:
        :returns:ifacenet: Devuelve la interfaz con la que se trabajara en ek equipo
        """
        try:
            file_config = "/etc/universalcheck/universalcheck.conf"
            config = ConfigParser()
            config.read(file_config)
            ifacenet = config.get('network_interface', 'niface')
            return ifacenet.strip()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    @staticmethod
    def init_program(log):
        """
        Funcion que devuelbe el dato del servicio que estara validando la aplicacion, mismo que se encuentra
        configurado en el archivo de texto.
        :returns:module: Regresa el valor del modulo con el que se estara trabajando.
        """
        try:
            file_config = "/etc/universalcheck/universalcheck.conf"
            config = ConfigParser()
            config.read(file_config)
            module = config.get('monitor', 'service_module')
            return module
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    @staticmethod
    def createMd5sum(files, log):
        chunk = 8192
        hasher = md5
        try:
            afile = open(files, 'rb')
            buf = afile.read(chunk)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(chunk)
            return hasher.hexdigest()

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))


class DataBase:
    '''Clase que contiene las funciones para manipular sqlite y realizar los diversos procesos en SQL.'''

    def __init__(self, log, db):
        """
        Funcion similar a un constructor el cual inicializa la variable db para uso en la clase.
        """
        self.db = db
        self.db_log = log

    # ---Query
    def dataSearch(self, statements, table, provisory, data):
        """
        Funcion que realiza un query o busqueda dentro de las tablas de la base de sqlite
        :param statements, table, provisory, data
        :returns: cursor, connection
        """
        global cursor, connection
        try:
            self.db_log.info_log("Iniciando la busqueda  en la base: %s " % self.db)
            connection = sqlite3.Connection(self.db)
            cursor = connection.cursor()

            if provisory != "" and data != "":
                statement = "SELECT " + statements + "  FROM " + table + provisory
                try:
                    cursor.execute(statement, data)
                except:
                    cursor.executescript(statement, data)
                return cursor, connection

            if provisory != "" and data == "":
                statement = "SELECT " + statements + "  FROM " + table + provisory
                try:
                    cursor.execute(statement)
                except:
                    cursor.executescript(statement)
                return cursor, connection

            if provisory == "":
                statement = "SELECT " + statements + "  FROM " + table
                try:
                    cursor.execute(statement)
                except:
                    cursor.executescript(statement)

                return cursor, connection

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.db_log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))
            cursor()
            connection.close()

            # ---Insert

    def insertion(self, table, statements, provisory, data):
        '''Funcion que realiza la inscersion de datos en una tabla de sqlite
        :param statements, table, provisory, data
        :returns: cursor, connection'''
        try:
            self.db_log.info_log("Insertando datos en la base: %s " % self.db)
            connection = sqlite3.Connection(self.db)
            cursor = connection.cursor()
            statement = "INSERT INTO " + table + statements + "VALUES" + provisory

            try:
                cursor.execute(statement, data)
            except:
                statement = "INSERT INTO " + table + statements + "VALUES" + " " + str(data)
                cursor.executescript(statement)
            connection.commit()
            cursor.close()
            connection.close()

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.db_log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))
            # ---Total

    def update(self, table, statements, provisory, data):
        '''Funcion que realiza la inscersion de datos en una tabla de sqlite
        :param statements, table, provisory, data
        :returns: cursor, connection'''
        try:
            self.db_log.info_log("Actualizando datos en la base: %s " % self.db)
            connection = sqlite3.Connection(self.db)
            cursor = connection.cursor()
            statement = "UPDATE  " + table + " SET " + statements + provisory
            #            print statement, data
            cursor.execute(statement, data)
            connection.commit()
            cursor.close()
            connection.close()

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.db_log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))
            # ---Total

    def total_data(self, column, table):
        '''Funcion que contabiliza el numero total de registros de en una tabla
        :param column, table
        :returns: total_column: Devuelve la totalidad de los datos validados'''
        try:
            self.db_log.info_log("Obteniendo el total de datos de la columna: %s de la base: %s " % (column, self.db))
            connection = sqlite3.Connection(self.db)
            cursor = connection.cursor()
            statement = "SELECT  COUNT(" + column + ") FROM " + table
            total_column = cursor.execute(statement)
            return int(total_column.fetchone()[0])

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.db_log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    def multi_data_insert(self, table, statements, provisory, information):
        '''Funcion realiza la insercion  de multiples registros  en una tabla
        :param table, statements, provisory, information
        :returns: cursor, connection'''
        try:
            self.db_log.info_log("Realizando la insercion de multiples datos: %s " % self.db)
            for data in information:
                self.insertion(table, statements, provisory, data)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.db_log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

            # ---Drop

    def table_delete(self, table):
        '''Funcion que borra una tabla de la base de datos
        :param table'''
        try:
            self.db_log.info_log("Borrando la tabla: %s " % table)
            connection = sqlite3.Connection(self.db)
            cursor = connection.cursor()

            statement = "DROP TABLE IF EXISTS  " + table
            cursor.execute(statement)
            ##        conn.commit()
            cursor.close()
            connection.close()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.db_log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    def data_erase(self, table, provisory):
        '''Funcion que borra datos de una tabla de la base de datos
        :param table, provisory
        '''
        try:
            self.db_log.info_log("Borrando datos de la tabla: %s " % table)
            connection = sqlite3.Conectiont(self.db)
            cursor = connection.cursor()
            statement = "DELETE FROM " + table + provisory
            cursor.execute(statement)
            cursor.close()
            connection.close()

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.db_log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

            # ---Create_table

    def create_table(self, table_name, values):
        '''Funcion para la creacion de una tabla en la base de datos
        :param table, values'''
        statement = "CREATE TABLE IF NOT EXISTS  " + table_name + values
        try:
            self.db_log.info_log("Creando la tabla: %s " % table_name)
            connection = sqlite3.Connection(self.db)
            cursor = connection.cursor()
            statement = "CREATE TABLE IF NOT EXISTS  " + table_name + values
            #            print statement
            try:
                cursor.execute(statement)
            except:
                statement = "CREATE TABLE IF NOT EXISTS  " + table_name + values
                cursor.executescript(statement)
            cursor.close()
            connection.close()

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.db_log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))

    def get_last_row(self, table):
        try:
            self.db_log.info_log("Buscando el ultimo elemento de la tabla: %s " % table)
            statements = " * "
            provisory = " WHERE Id=(SELECT MAX(Id) FROM " + table + ")"
            result = self.dataSearch(statements=statements, table=table, provisory=provisory, data="")
            last_row = result[0].fetchone()
            result[1].close()
            return last_row
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.db_log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))


class Create_Table:
    '''Clase auxiliar para la creacion de la tabla y el archivo bitacora de la aplicacion'''

    def __init__(self, log, db_file):
        '''Funcion similar a un constructor, se inicializan las variables de clase file_db que contiene la ubicacion
        de el archivo sqlite asi tambien se inicializa una variable objeto de la clase DataBase para realizar la
        creacion de la tabla de Daros de universalcheck'''
        self.file_db = db_file
        self.db = DataBase(log, db_file)

    def init_db(self, log):
        '''Funcion que valida si existe el archivo de sqlite que seran las bitacoras, si existe no realiza la creacion,
        de la tabla ya que se da por entendido que ya debio crearce si no existe el archivo lo crea y crea la tabla.'''
        try:
            if os.path.exists(self.file_db):
                pass
            else:
                TABLE = "logbook"
                STATEMENTS = '''(Id INTEGER PRIMARY KEY AUTOINCREMENT, Hostname VARCHAR(50), Date VARCHAR(50),
                Time VARCHAR(50), Status VARCHAR(50))'''
                self.db.create_table(TABLE, STATEMENTS)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error_log("Se precento el error: %s %s %s0" % (exc_type, exc_value, exc_traceback))
