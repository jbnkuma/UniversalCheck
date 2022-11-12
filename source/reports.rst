Instalación de rpm reports.rpm
==============================

1.Requerimientos.
-----------------
Para realizar este procedimiento se debe tener el paquete, con el siguiente md5sum:

* python => 2.6.
* universalcheck => 1.2-4


2.Instalación
-------------
Una vez que se tenga el paquete se debe realizar en linea de comandos el siguiente procedimiento:

.. code-block:: bash
    :linenos:

                rpm -ivh reports-1.1.0-5.noarch.rpm

2.1 Actualización
-----------------
Una vez que se tenga el paquete se debe realizar en linea de comandos el siguiente procedimiento:

.. code-block:: bash
    :linenos:

            rpm -Uvh reports-"version".noarch.rpm



    Donde "versión" es la versión del paquete que actualizara el ya instalado en el sistema.

3.Configuración
---------------

La aplicación reports usa los archivos de configuración de universalchek, el cual se encuentra ubicado
en /etc/ y tiene la siguiente estructura:

    /etc/
        universalcheck/
                      universalcheck.conf
    /etc/
        universalcheck/
                      servers.json

El archivo universalcheck.conf es el archivo donde se tienen la configuraciones de funcionamiento de universalcheck,
mismo que reports usa para la busqueda de downtimes en base al servicio que se este monitoreando con univesalchek
por lo que este archivo se debera editar con previa autorización y una vez que se realicen pruebas antes de las edición.


4.Funcionamiento
----------------
El funionamiento del script del paquete reports es el siguiente:

1) Sin argumentos:
    .. code-block:: bash
        :linenos:

                /usr/bin/server_reports


        .. image:: reports.png
:height: 80px
        :width: 1150 px
            :scale: 90 %
            :alt: alternate text
            :align: left


        Cuando es ejecutado el script server_reports sin argumentos realiza la contabilización total de downtimes en las bitacoras
    del universalcheck, en primera instancia revisa los archivos .db creados en directorio /var/log/availability/diamesaño/,
    en caso de que la carpeta no exista realiza la busqueda en /var/log/availability/ en las bitacoras que ahi se generan,
    para entregar al cliente, esta contabilización es solo por el día en el que fue invocado el script con la restricción
    de que el resultado es calculado del momento de ejcución menos una hora, esto debido a que en el momento en que se
    ejecute el script server_reports es probable que la bitacora de universalcheck  en el momento de ejecucíon se encuentre
    incomplento por que aún no a trascurrido la hora para cerrar la bitacora, con esto se evitan falsos positivos.


    2) Con argumentos:
        .. code-block:: bash
            :linenos:

                /usr/bin/server_reports 01-06-2015 30-06-2015

    El script server reports acepta como parametros un rango de fechas unicamente (fecha_inicio, fecha_final) cuando es
    ejecutado el script server_reports de esta manera realiza el mismo proceso anteriormente descrito en busca de
    downtimes en las bitacoras de universalcheck, en el rango de fechas que se han introducido como argumentos  del script
    el resultado es el numero total de downtimes en el rango de las fechas introducidas.

    La ejecución de server_reports requiere privilegios por lo que se a añadido una entrada en el archivo sudoers, la cual
    es la siguiente: "univcheck ALL=NOPASSWD: /usr/bin/server_reports", permitiendo que pueda ejecutarse sin inconvenientes,
    esto esta añadido en el rpm de instalación por lo que no es necesario una intervencion manual.

    Este script sera ejecutado de forma automatica desde el servidor central, el cual se encargara de guardar los resultados,
    obtenidos de downtimes y almacenarlo para preparar el reporte mensual del SLA.


5.Logs de funcionamiento
------------------------
La ejecución del script server_reports genera una bitacora de funcionamiento en el directorio /var/log/slamon/ en el archivo:
reports.log, en el cual se puede visualizar las etapas de ejecución para la obtención del total de downtimes, tambien en
este archivo se puden visualizar los errores ocurridos en tiempo de ejecución, por lo que este archivo es necesario sea,
revisado en caso de mal funcionamiento para diagnosticar algun problema.
