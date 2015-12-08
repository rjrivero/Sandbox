Rol GNS3
========

Este rol provisiona una maquina virtual creada mediante vagrant, instalando:

  - [X2Go](http://wiki.x2go.org/doku.php)
  - [GNS3](http://www.gns3.com/)
  - [Juniper vMX](http://www.juniper.net/techpubs/en_US/vmx15.1/topics/concept/vmx-overview.html)

La configuración del hardware virtual (número de vCPUs, memoria, interfaces de red, etc) está el Vagrantfile de [vagrant/gns3](../../../vagrant/gns3/README.md). Este playbook se encarga de:

  - Instalar los paquetes necesarios.
  - Configurar X2Go y configurar las claves publicas
  - Configurar una topología vMX.

Preparación
-----------

Antes de poder provisionar el servidor GNS3, es necesario bajarse la [imagen de vMX de Juniper](https://www.juniper.net/support/downloads/?p=vmx#sw), y guardarla en el directorio **files** del rol.

La imagen tiene dos números que hay que utilizar para configurar el rol:

  - La version de vmx, que esta en el propio nombre del fichero (vmx-**15.1F3.11**.tgz)
  - La versión de vFC, a la que para complicarnos un poco la vida a los devops, le añaden la fecha (vmx-15.1F3.11/images/vFPC-**20151017**.img)

La versión de vFC puede encontrarse mirando dentro del paquete comprimido, con:

```
tar -tzvf vmx-*.tgz | grep vFP
```

Una vez descargado el software al directorio *playbooks/roles/gns3/files* y encontrados los dos numeros de version, se debe configurar el rol.

Configuración
-------------

El espacio de swap en el servidor virtual GNS3 se configura en el fichero [meta/main.yml](meta/main.yml), a través de la herencia con el rol [KVM](../kvm/README.md).

El puerto en el que escucha X2Go se configura en [el Vagrantfile](../../../vagrant/gns3/Vagrantfile), con port_forwarding. Por defecto, es el 10000.

El resto de configuraciones se hacen a través del fichero [vars/main.yml](vars/main.yml):

  - Versiones de software de vMX y vFC (obligatoria).
  - Definición de instancias de vMX (nombres, interfaces, MACs...)
  - Enlaces entre instancias vMX

El script copia las claves públicas autorizadas (*~/.ssh/authorized_keys*) del host al guest, asi que para poder iniciar sesion en la maquina GNS3 con X2Go, basta con añadir la clave publica ssh del cliente al fichero authorized_keys del host, y reprovisionar.

```
echo <CLAVE_PUBLICA_SSH> >> ~/.ssh/authorized_keys
vagrant provision
```

Consumo de recursos
-------------------

Este servicio consume bastante memoria. Cada instancia de vMX crea dos máquinas virtuales con 512MB de RAM cada una, por lo que cada router virtual requiere en total algo más de 1GB (contando con el overhead de KVM).

El tamaño de memoria y número de vCPUs asignado a cada instancia de vMX se configura en el fichero [templates/vmx.conf](templates/vmx.conf).

Gestion
-------

Para poder acceder el entorno de laboratorio desde el servidor (host), el [rol vagrant](../vagrant/README.md) crea una interfaz de red **vMX_mgmt**, a la que se conectan todas las interfaces de gestión fuera de banda de todos los routers. De esta forma, se puede acceder a los routers:

  - Desde el host (fuera de la maquina vagrant), a través de la interfaz vMX_mgmt (**192.168.199.1**)
  - Desde el guest (creado por Vagrant), a través de la interfaz eth1 (**192.168.199.10**)

Las direcciones IP de la red de gestión están fijadas manualmente en el fichero [files/net_mgmt.xml del rol vagrant](../vagrant/files/net_mgmt.xml), y en [el Vagrantfile](../../../vagrant/gns3/Vagrantfile), y no son configurables. Las direcciones de gestión de las instancia vMX creadas en el fichero [vars/main.yml](vars/main.yml) **deben pertenecer a la misma red 192.168.199.0/24**.

Etiquetas
---------

El playbook utiliza las siguientes etiquetas:

  - **packages**: Para la instalación de los paquetes del sistema operativo.
  - **vmx**: Para la instalación y configuración de vmx
  - **x2go**: Para la instalación y configuración de X2Go

Arranque de las máquinas
------------------------

El primer arranque de las instancias de vMX es pesado y lento. Tanto es así que no he querido que los scripts de provisión las arranque, sino que he preferido dejar el proceso manual.

Una vez completada la creación de la máquina virtual con Vagrant y su provisión,deberán arrancarse manualmente las instancias de vMX con los comandos:

```
# Dentro del directorio vagrant/gns3
vagrant ssh

# Una vez conectado a la máquina virtual
cd /opt/vmx/vmx*
sudo ./vmx.sh -lv --install --cfg config/vmx-<nombre_de_instancia>.cfg
```

El script **vmx.sh** crea la instancia de vMX. El flag *-lv* activa el debug, y el flag *--install* la instalación.

Por cada instancia de vMX definida en el fichero [vars/main.yml](vars/main.yml), habrá un fichero de configuración vmx-**nombre_de_instancia**.cfg que será necesario ejecutar con *vmx.sh*.

Para ver como avanza la instalación de una instancia, se puede abrir la consola con el comando

```
./vmx.sh --console vpc <nombre de instancia>
```

El login es **root**, sin password. Se entra en modo comando con *cli*, y se pueden ver las interfaces creadas con *show interfaces terse*. Para salir de la consola de una instancia vMX, pulsar Ctrl+] y teclear "quit" cuando se muestre el prompt *telnet>*.

Cada máquina que complete su instalación se puede apagar y volver a encender con *./vmx.sh stop* o *start*.

Por último, una vez arrancadas todas las máquinas, hay que ejecutar:

```
sudo ./vmx.sh --bind-dev
```

Esto enlaza las interfaces virtuales de las instancias vMX entre sí, y con los puertos del host, de acuerdo con la configuración que se haya definido en [vars/main.yml](vars/main.yml).

