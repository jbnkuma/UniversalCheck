Script hash_logs
================

1.Requerimientos.
-----------------
Es parte del paquete universalcheck, por lo que son los mismos requerimientos de instalación

3.Configuración
---------------
La configuracíon del script es hard-code por lo que en caso de ser necesario se deben editar las variables de los,
directorios en el codigo fuente del script

4.Funcionamiento
----------------
El funionamiento del script  hash_logs es el siguiente:

Cada hora se ejecuta el script, realizando el calculo del md5sum de las bitacoras creadas por el universalcheck y
escribiendo el md5 en un archivo txt con el mismo nombre de la bitacora, dejando disponible el archivo txt y el archivo
de la bitacora disponible para que el cliente recoja ambos archivos.

Se encuentra en:

.. code-block:: bash
            :linenos:

                /usr/bin/hash_logs


5.Logs de funcionamiento
------------------------
La ejecución del script hash_logs genera una bitacora de funcionamiento en el directorio /var/log/slamon/ en el archivo:
md5sum_sla.log, en el cual se puede visualizar las etapas de ejecución para la obtención del md5sum de las bitacoras,
tambien en este archivo se puden visualizar los errores ocurridos en tiempo de ejecución, por lo que este archivo es
necesario sea, revisado en caso de mal funcionamiento para diagnosticar algun problema.
