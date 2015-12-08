Servidor de escritorio remoto por HTML
====================================

Este rol instala un servicio de escritorio remoto [Guacamole](http://guac-dev.org/) para acceder via HTML a los escritorios de las maquinas virtuales instaladas en este servidor.

El servicio se instala como un contendor docker con los siguientes parametros:

  - nombre: guacamole
  - puerto: 8080
  - usuario: vnc
  - contraseña: $VNC_PASSWORD

La contraseña es la variable de entorno **VNC_PASSWORD** que debe establecerse antes de ejecutar el script:

```
# Dejar un espacio al principio de la linea de comandos, para que no se grabe
 export VNC_PASSWORD="Changeme!"
ansible-playbook -t guacamole bootstrap.yml
```
Volumenes
---------

La configuracion del servicio se guarda en **/opt/guacamole**. Este directorio se monta como el volumen **/etc/guacamole** dentro del contenedor.
