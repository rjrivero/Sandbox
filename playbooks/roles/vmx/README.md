Rol GNS3
========

Este rol provisiona una maquina virtual creada mediante vagrant, instalando el software [Juniper vMX](http://www.juniper.net/techpubs/en_US/vmx15.1/topics/concept/vmx-overview.html)

La configuración del hardware virtual (número de vCPUs, memoria, interfaces de red, etc) está el Vagrantfile de [vagrant/gvmx](../../../vagrant/vmx/README.md). Este playbook se encarga de:

  - Instalar los paquetes necesarios.
  - Configurar una topología vMX.

Preparación
-----------

Antes de poder provisionar el servidor, es necesario bajarse la [imagen de vMX de Juniper](https://www.juniper.net/support/downloads/?p=vmx#sw), y guardarla en el directorio **files** del rol.

La imagen tiene dos números que hay que utilizar para configurar el rol:

  - La version de vmx, que esta en el propio nombre del fichero (vmx-**14.1R6.4**.tgz)
  - La versión de vFC, a la que para complicarnos un poco la vida a los devops, le añaden la fecha (vmx-154.1R6.4images/vFPC-**220151026**.img)
:spl
La versión de vFC puede encontrarse mirando dentro del paquete comprimido, con:

```
tar -tzvf vmx-*.tgz | grep vFP
```

Una vez descargado el software al directorio *playbooks/roles/vmx/files* y encontrados los dos numeros de version, se debe configurar el rol.

Configuración
-------------

El espacio en swap en el servidor virtual GNS3 se configura con los parametros **swap_path**, **swap_megas** y **swap_crypt** del rol [KVM](../kvm/README.md). El resto de configuraciones se hacen a través del fichero [vars/main.yml](vars/main.yml):

  - Versiones de software de vMX y vFC (obligatoria).
  - Definición de instancias de vMX (nombres, interfaces, MACs...)
  - Enlaces entre instancias vMX

Consumo de recursos
-------------------

Este servicio consume bastante memoria. Cada instancia de vMX crea dos máquinas virtuales con 1GB (control Plane) y 6GB (Forwarding Plane) de RAM, por lo que cada router virtual requiere en total algo más de 17GB (contando con el overhead de KVM).

El tamaño de memoria y número de vCPUs asignado a cada instancia de vMX se configura en el fichero [templates/vmx.conf](templates/vmx.conf).

Gestion
-------

Las dos maquinas virtuales que crea el script vmx.sh (la de control y la de forwarding) tienen una direccion IP en el rango de la interfaz eth0 del host. Esto debe ser asi para que el montaje funcione.

Al usar como host una maquina virtual creada con el proveedor de libvirt para Vagrant, la interfaz eth0 se enlaza a una red virtual **vagrant-libvirt** con el direccionamiento por defecto **192.168.121.0/24**. Las direcciones de gestión de las instancia vMX definidas en el fichero [vars/main.yml](vars/main.yml) **deben pertenecer a la misma red 192.168.121.0/24**.

Ademáde esa red, cada máina virtual tiene una segunda interfaz **eth1** que pertenece a la red de gestion [vMX_mgmt del rol Vagrant](../vagrant/files/net_mgmt.xml). La direccion de esa interfaz se configura en [el Vagrantfile](../../../vagrant/vmx/Vagrantfile).

Etiquetas
---------

El playbook utiliza las siguientes etiquetas:

  - **packages**: Para la instalación de los paquetes del sistema operativo.
  - **vmx**: Para la instalación y configuración de vmx

Arranque de las máquinas
------------------------

El primer arranque de las instancias de vMX es pesado y lento. Tanto es así que no he querido que los scripts de provisión las arranque,n sino que he preferido dejar el proceso manual.

Una vez completada la creación de la máquina virtual con Vagrant y su provisión,deberán arrancarse manualmente las instancias de vMX con los comandos:

```
# Dentro del directorio vagrant/vmx
# "vagrant ssh" es "arriesgado" porque al hacer la instalacion de la maquina
# virtual, el script crea un bridge y mueve la interfaz eth0 a dicho bridge,
# lo que puede provocar que se pierda la conexion y se interrumpa el script.
# Por este motivo, se recomienda mejor hacer un SSH a la direccion IP asignada
# a la interfaz eth1 de la maquina:
ssh-keygen -f "~/.ssh/known_hosts" -R 192.168.199.10
ssh -a -l vagrant 192.168.199.10

# Una vez conectado a la máquina virtual
cd /opt/vmx/vmx*
sudo ./vmx.sh -lv --install --cfg config/vmx-<nombre_de_instancia>.cfg
```

El script **vmx.sh** crea la instancia de vMX. El flag *-lv* activa el debug, y el flag *--install* la instalación.

Por cada instancia de vMX definida en el fichero [vars/main.yml](vars/main.yml), habrá un fichero de configuración vmx-**nombre_de_instancia**.cfg que será necesario ejecutar con *vmx.sh*.

Para ver como avanza la instalación de una instancia, se puede n abrir las consolas del control plane y el forwarding plane respectivamente con los comandos:

```
./vmx.sh --console vcp <nombre de instancia> # control plane
./vmx.sh --console vfp <nombre de instancia> # Forwarding plane
```

El login del control plane es **root**, sin password. Se entra en modo comando con *cli*. el login del forwarding plane es **root** con password **root**. Para salir de la consola de una instancia vMX, pulsar Ctrl+] y teclear "quit" cuando se muestre el prompt *telnet>*.

La instalacion tarda mucho. Mucho es **MUCHO**, puede tirarse tranquilamente media hora. Lo mejor es monitorizar el estado desde la vCP, ejecutando ocasionalmente el comando *show chassis 0 fpc detail*, hasta que la placa lleve ya un ratito **online**:

```
root> show chassis fpc 0 detail
Slot 0 information:
  State                                 Online
  Temperature                        Absent
  Total CPU DRAM                      0 MB
  Total RLDRAM                        0 MB
  Total DDR DRAM                      0 MB
  Start time:                           2016-01-04 15:55:42 UTC
  Uptime:                               4 minutes, 16 seconds
  Max Power Consumption               0 Watts
```

Cuando la tarjeta haya sido reconocida y este online, es recomendable **reiniciar las dos maquinas virtuales desde sus respectivas consolas**, para que cojan las configuraciones finales y funcione por fin...

Cada máquina que complete su instalación se puede apagar y volver a encender con *./vmx.sh --stop* o *--start*.

Por último, una vez arrancadas todas las máquinas, hay que ejecutar:

```
sudo ./vmx.sh --bind-dev
```

Esto enlaza las interfaces virtuales de las instancias vMX entre sí, y con los puertos del host, de acuerdo con la configuración que se haya definido en [vars/main.yml](vars/main.yml).

