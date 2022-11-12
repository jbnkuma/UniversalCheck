Instalación de rpm universalcheck.rpm y reports.rpm
===================================================

1.Requerimientos.
-----------------
Para realizar este procedimiento se debe tener el paquete universalcheck, con el siguiente md5sum y cumplir con las
siguientes dependencias:

SLES 11 y SLES 12.

* python => 2.6.
* curl.
* openldap2-client.
* bash.
* procps.
* coreutils.
* iproute2.
* netcat.

SLES 10.

* python => 2.3.
* curl.
* openldap2-client.
* bash.
* procps.
* coreutils.
* iproute2.
* netcat.
* pyuuid
* simplejson

En el caso del rpm reports la unica dependencia es tener previamente instalado el rpm universalcheck > 1.2-4


Una vez  realizada la instalación y configuración debemos comentar la linea del crontab que mantiene activo al script
universalcheck.sh, mediante el comando siguiente:

.. code-block:: bash
    :linenos:

         crontab -l

    dando como resultado lo siguiente:

.. image:: crontab.png
:height: 180px
   :width: 1200 px
       :scale: 60 %
       :alt: alternate text
       :align: center

    Como se puede apreciar en este servidor se tiene el universalcheck.sh monitoreando el servicio de lag (el script ya fue comentado)

    Instalación

    SLES 11

.. code-block:: bash
    :linenos:

               eaaa48603d075cfb55d4cfd8a0e16057  universalcheck-1.2-10.noarch.rpm
               f60b91b28309a1de1e55ed721784251e  reports-1.1.0-5.noarch.rpm
    SLES 10

.. code-block:: bash
    :linenos:

               376880cd291cd4e9226a827e29a2c377  universalcheck-1.2-10.noarch.rpm
               bcd5bec8a33fdce6dfa6788f0b1ba5e7  reports-1.1.0-5.noarch.rpm

2.Instalación
-------------
Una vez que se tenga el paquete se debe realizar en linea de comandos el siguiente procedimiento:

.. code-block:: bash
    :linenos:

              rpm -ivh universalcheck-1.2-7.noarch.rpm reports-1.1.0-5.noarch.rpm



    Para el caso de SLES 10 se tiene dos archivos adicionales que deben ser instalados:

    * pyuuid-0.0.1-11.x86_64.rpm
    * simplejson-2.0.5.tar.gz

    El primero  se debe instalar  como comunmente se instalan los rpm.

.. code-block:: bash
    :linenos:

              rpm -ivh pyuuid-0.0.1-11.x86_64.rpm


    Para el paquete simplejson-2.0.5.tar.gz se debe instalar con los siguientes privilegios, de la siguiente forma:


.. code-block:: bash
    :linenos:

            tar -xvzf simplejson-2.0.5.tar.gz
            cd simplejson-2.0.5
            python setup.py build
            python setup.py install



2.1 Actualización
-----------------
Una vez que se tenga el paquete se debe realizar en linea de comandos el siguiente procedimiento, los paquetes
dependencia se entiende que ya debieron ser instalados en la anterior version de no ser el caso se procede como si
fuera una nueva instalación:

Verificando versión instalada:

.. image:: rpmqa.png
:height: 200px
   :width: 900 px
       :scale: 60 %
       :alt: alternate text
       :align: center

    Realizando la actualización:

.. code-block:: bash
    :linenos:

              rpm -Uvh universalcheck-"version".noarch.rpm reports-"version".noarch.rpm

    Donde "versión" es la versión del paquete que actualizara el ya instalado en el sistema.

2.2 Re-instalación
------------------
En caso de ser necesaria una reinstalación del paquete mientras ya se tiene una versión instalada se debe realizar el
procedimiento siguiente:

* Remover el paquete universalcheck:

.. code-block:: bash
    :linenos:

              zypper remove universalcheck


    *Realizar el proceso de instalación descrito en este documento


3.Configuración
---------------

La aplicación cuenta con un directorio donde se tienen los archivos de configuración, el cual se encuentra ubicado
en /etc/ y tiene la siguiente estructura:

    /etc/
        universalcheck/
                      universalcheck.conf
    /etc/
        universalcheck/
                      servers.json

El archivo universalcheck.conf es el archivo donde se tienen la configuraciones de funcionamiento de universalcheck,
por lo que este se debera editar con previa autorización y una vez que se realicen pruebas antes de las edición.

.. code-block:: bash
    :linenos:

                        /etc/universalcheck/universalcheck.conf



    El contenido del archivo es el siguiente:

.. code-block:: bash
    :linenos:

                #Comandos usados en las validaciones de los servicios, NO editar a menos de que se tenga previa autorización
                #y validaciones  de los comandos que se coloquen en este apartado
                [comandoschek]
                      edir = ldapsearch -LLL -x -h localhost -p 389 -D cn=sla_proxy,ou=servicios,o=sat -w 5L4_pR0xY-F0cu5% -b cn=sla_proxy,ou=servicios,o=sat cn
                  clagheartbeat = curl -o /dev/null --connect-timeout 4 -s -w '%{http_code},%{time_total}'
                  csatc8080 = curl -o /dev/null --connect-timeout 4 -s -w 'HTTP %{http_code}, %{time_total}s'
                  cSuperLumin = netcat -nvz
                  #Ubicacion del archivo con los datos de servidores LAG y LAGE no editar sin previa autorización.
                  [dbconf]
                      jsonfile = /etc/universalcheck/servers.json
                  #Intefaz de red  de red de administración editar en caso necesario.
                [network_interface]
                       niface = eth0
                   #Servicio que sera monitoreado editar en caso de ser necesario.
                [monitor]
                   service_module = edir389

                   Se debe verificar que la interfaz de red sea la correcta, asi como el servicio que se va a monitorear, en caso de ser
                   necesario se debe editar  el valor de service_module de la seccion monitor manteniendo el formato que se observa en el
                   archivo

    Los posibles valores para service_module son los que se listan a continuación:

        * edir389
        * lagherbeat
        * lagherbeattmp
        * idpheartbeat
        * tomcat_imanager
        * satcserv
        * satauth
        * ciecinter
        * ciecintra
        * wsau
        * wsfe
        * superlumin
        * nagios
        * nagios_noc
        * server_uptime


    El archivo servers.json es el archivo donde se tienen los datos de los servidores lag y lage , por lo que este se
    debe editar una vez que se pretenda monitorear alguno de los dos servicios mencionados, la edicion de este archivo .
    debera realizarse solo en caso de que en el proceso de instalación la autoconfiguración falle, ya que de manera
    automatica al instalar se realiza la configuracíon de los datos para un servidor lag.

.. code-block:: bash
    :linenos:

                            /etc/universalcheck/servers.json

    El contenido y  formato del archivo es el siguiente:

.. code-block:: bash
    :linenos:

                {
                     "tqidnproagqc01": {
                     "ip": "'10.56.80.157'",
                     "port": "443"
                                    }
                }

    Este formato debe mantenerse tal como se muestra, teniendo el hostname, la ip y el puerto, del servidor que se va
    monitorear.




5.Logs de funcionamiento
------------------------
La ejecución del script universalchek genera una bitacora de funcionamiento en el directorio /var/log/slamon/ en el archivo:
universalcheck.log, en el cual se puede visualizar las etapas de ejecución del monitoreo de las aplicaciónes
este archivo se puden visualizar los errores ocurridos en tiempo de ejecución, por lo que este archivo es necesario sea
revisado en caso de mal funcionamiento, para diagnosticar algun problema.

En este mismo directorio se tiene el log para el script server_reports el cual lleva por nombre reports.log  por lo que
este archivo es necesario sea revisado en caso de mal funcionamiento, para diagnosticar algun problema.






