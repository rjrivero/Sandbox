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

Servicios
---------

Los servicios que están actualmente integrados en este playbook son

  - Servidor [vagrant](https://www.vagrantup.com/). El playbook *bootstrap.yml* configura al equipo como un servidor Vagrant con el proveedor [libvirt](https://github.com/pradels/vagrant-libvirt). Este servicio está compuesto por [el rol vagrant](playbooks/roles/vagrant/README.md).

  - Servidor GNS3. Este servicio está compuesto por [el rol gns3](playbooks/roles/gns3/README.md) y [un Vagrantfile](vagrant/gns3/README.md).
