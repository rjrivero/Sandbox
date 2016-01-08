Rol GNS3
========

Este rol provisiona instala y configura:

  - [X2Go](http://wiki.x2go.org/doku.php)
  - [GNS3](http://www.gns3.com/)

El playbook se encarga de:

  - Instalar los paquetes necesarios.
  - Configurar X2Go y GNS3.
  - Copiar el fichero *authorized_keys* del host, para que se pueda iniciar sesion en X2Go utilizando los mismos certificados que se usan para acceder a la maquina desde la que se lanza el playbook.

Configuración
-------------

El script copia las claves públicas autorizadas (*~/.ssh/authorized_keys*) del host al guest, asi que para poder iniciar sesion en la maquina GNS3 con X2Go, basta con añadir la clave publica ssh del cliente al fichero authorized_keys del host, y reprovisionar.

```
echo <CLAVE_PUBLICA_SSH> >> ~/.ssh/authorized_keys
# Si el servidor GNS3 se gestiona con Vagrant
vagrant provision
```

Etiquetas
---------

El playbook utiliza las siguientes etiquetas:

  - **packages**: Para la instalación de los paquetes del sistema operativo.
  - **x2go**: Para la instalación y configuración de X2Go
  - **gns3**: Para la instalacion de los paquetes de GNS3.

