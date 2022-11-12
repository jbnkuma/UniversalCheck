Instalación de rpm universalcheck.rpm
=====================================


1.Requerimientos.
-----------------
Para realizar este procedimiento se debe tener el paquete  universalcheck-1.0-4.noarch.rpm, que a su vez requiere de los
siguientes paquetes:

-python => 2.6.
-curl.
-openldap2-client.
-bash.
-procps.
-coreutils.
-iproute2.
-netcat.

2.Instalación
-------------
Una vez que se tenga el paquete se debe realizar en linea de comandos el siguiente procedimiento:

.. code-block:: bash
    :linenos:

                        rpm -ivh universalcheck-1-1.noarch.rpm

2.1 Actualización
-----------------
Una vez que se tenga el paquete se debe realizar en linea de comandos el siguiente procedimiento:

.. code-block:: bash
    :linenos:

                        rpm -Uvh universalcheck-"version".noarch.rpm

            Donde "versión" es la versión del paquete que actualizara el ya instalado en el sistema.

3.Configuración
---------------

La aplicación cuenta con un archivo de configuracíon el cual se encuentra ubicado en /etc/universalcheck/, el nombre
de dicho archivo es universalcheck.conf.

 Siendo su contenido como acontinuación se define:

 .. code-block:: bash
    :linenos:

                        #Comandos usados en las validaciones de los servicios, NO editar a menos de que se tenga previa autorización
                        #y validaciones  de los comandos que se coloquen en este apartado
                        [comandoschek]
                            edir = ldapsearch -LLL -x -h localhost -p 389 -D cn=nts_proxy,ou=servicios,o=sat -w 4gr33 -b cn=nts_proxy,ou=servicios,o=sat cn
                            clagheartbeat = curl -o /dev/null --connect-timeout 4 -s -w '%{http_code},%{time_total}'
                            csatc8080 = curl -o /dev/null --connect-timeout 4 -s -w 'HTTP %{http_code}, %{time_total}s'
                            cSuperLumin = netcat -nvz
                            #Ubicacion del archivo con los datos de servidores LAG y LAGE no editar sin previa autorización.
                        [dbconf]
                            dbfile = /etc/universalcheck/servers.db
                        #Intefaz de red  de red de administración editar en caso necesario.
                        [network_interface]
                            niface = wlp2s0b1
                        #Servicio que sera monitoreado editar en caso de ser necesario.
                        [monitor]
                            service_module = edir389

                     Se debe verificar que la interfaz de red sea la correcta asi como el servicio que se va a monitorear, en caso de ser
                     necesario se debe editar  el valor de service_module de la seccion monitor, los posibles valores para esta variable son:

                    * edir389
                    * lagherbeat
                    * lagherbeattmp
                    * idpheartbeat
                    * tomcat_imanager
                    * indexauth
                    * satcserv
                    * satauth
                    * indexciec
                    * ciecinter
                    * ciecintra
                    * wsau
                    * wsfe
                    * superlumin
                    * nagios
                    * nagios_noc
                    * server_uptime

                    Se debe colocar alguno de estos valores dependiendo el servicio que se validara.