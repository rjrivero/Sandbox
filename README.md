Repositorio de servidor personal
================================

Repositorio donde voy guardando todos los servicios que despliego en
el servidor de prueba.

Quick Start
-----------

Para inicializar un servidor, de forma que pueda usar el repositorio:

  - Configurar passwordless sudo y ssh con certificados

```
export USERNAME=`id -un`
echo "$USERNAME ALL = (ALL) NOPASSWD:ALL" | sudo tee "/etc/sudoers.d/$USERNAME"
sudo chmod 0600 "/etc/sudoers.d/$USERNAME"

ssh-keygen -t rsa -b 4096 -C "private@email.com"
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

  - Instalar los paquetes virtualenv, python-dev y build-essentials

```
sudo apt-get update
sudo apt-get install git python-virtualenv python-dev build-essential
```

  - Crear el virtualenv e instalar ansible

```
export VIRTUALENV_DIR=~/manage
virtualenv --system-site-packages "$VIRTUALENV_DIR"

cd "$VIRTUALENV_DIR"
git clone git://github.com/ansible/ansible.git --recursive
```

  - En el mismo directorio, descargar el repo e iniciar el entorno

```
git clone https://github.com/rjrivero/Sandbox inventory
source inventory/init.sh -U
```

  - Ejecutar la config inicial del servidor

```
ansible-playbook inventory/playbooks/bootstrap.yml
```

Cifrado de disco
----------------

El servidor puede configurarse para que disponga de un grupo de volumenes
**tank**, cifrado (basado en LVM+luks), donde almacenar la información
sensible; típicamente se crearían en ese grupo volúmenes para
**/var/lib/docker** y **/opt**

Particionar el disco e inicializar el volumen cifrado son tareas difíciles
de conseguir de forma idempotente en un playbook, por eso esas tareas se han
quedado fuera de estos scripts y hay que hacerlas a mano.

El trabajo manual que hay que hacer se reduce a:

  - Inicializar un disco o partición con luks, creando una clave de descifrado.

```
# Hacer un borrado seguro. Ver 
# https://wiki.archlinux.org/index.php/Dm-crypt/Drive_preparation
# ---------------------------------------------------------------

# Creamos dispositivo temporal
sudo cryptsetup open --type plain <dispositivo> container --key-file /dev/urandom

# Comprobamos que se ha montado
sudo fdisk -l | grep container

# Randomizamos el contenido
sudo dd if=/dev/zero of=/dev/mapper/container status=progress

# Si la version de dd no soporta "status=progress", se puede ejecutar
# en otra ventana, para monitorizar el progreso de dd:
watch -n5 'sudo kill -USR1 $(pgrep ^dd)'

# Cerramos el dispositivo
sudo cryptsetup close container

# Hacer la configuracion definitiva con las claves finales
# --------------------------------------------------------

sudo cryptsetup luksFormat -c aes-xts-plain64 -s 512 -h sha512 <dispositivo>
```

  - Configurar el playbook de despliegue con el nombre del dispositivo cifrado, definienndo la variable **crypt_device** en el playbook [bootstrap.yml](playbooks/bootstrap.yml).

**NOTA IMPORTANTE**: Por seguridad, la clave de cifrado no se guarda en ningún sitio, por lo que el arranque del sistema operativo no puede depender del volumen cifrado; de otro modo, se quedaría bloqueado esperando la clave de descifrado.

Esto implica que:

  - El swap **No puede ser** un volumen lógico dentro del disco cifrado; tiene qu eestar fuera. El [rol KVM](playbooks/roles/kvm/README.md) acepta los parámetros *swap_path* y *swap_crypt* que permiten crear un fichero de swap cifrado en una ruta cualquiera, dentro de una partición no cifrada.

  - Si */var/lib/docker* se monta desde un volumen LVM, entonces el servicio *docker* **no puede estar configurado para arrancar automáticamente**. Debe iniciarse manualmente, una vez se haya descifrado y montado el dispositivo.

Cada vez que se reinicie el servidor, será necesario abrir manualmente el dispositivo cifrado, y ejecutar el **playbook bootstrap.yml**, para que monte todos los dispositivos e inicie los servicios necesarios.

```
# Abrir el dispositivo. Por convencion, lo llamaremos "tank".
sudo cryptsetup open <ruta al dispositivo> tank

# Montar los volumenes e iniciar los servicios
cd inventory/playbooks
source ../init.sh
ansible-playbook bootstrap.yml
```

Servicios
---------

Los servicios que están actualmente integrados en este playbook son

  - Servidor [vagrant](https://www.vagrantup.com/). El playbook *bootstrap.yml* configura al equipo como un servidor Vagrant con el proveedor [libvirt](https://github.com/pradels/vagrant-libvirt). Este servicio está compuesto por los roles:

    - [Vagrant](playbooks/roles/vagrant/README.md).
    - [Docker](playbooks/roles/docker/README.md).

  - Servidor GNS3. Este servicio está compuesto por [el rol gns3](playbooks/roles/gns3/README.md) y [un Vagrantfile](vagrant/gns3/README.md).
