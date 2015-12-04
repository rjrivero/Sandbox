Rol de servidor Vagrant
=======================

Este rol instala el paquete vagrant de https://www.vagrantup.com/. Junto con vagrant, se instalan los plugins:

  - [vagrant-libvirt](https://github.com/pradels/vagrant-libvirt), para poder ejecutar maquinas virtuales con KVM en lugar de VirtualBox.
  - [vagrant-mutate](https://github.com/sciurus/vagrant-mutate), para convertir boxes de VirtualBox a formato KVM.

Además, crea una red de administración **vMX_mgmt** para las interfaces de gestión fuera de banda de los routers virtuales del [servicio gns3](../gns3/README.md). Tengo que hacero aqui, no puedo hacerlo en el propio rol **gns3** porque ese rol solo se ejecuta dentro de la maquina vagrant.

Configuracion
-------------

El rol hereda de [KVM](../kvm/README.md), que le permite especificar el tamaño y la ruta del espacio de swap en el fichero [meta/main.yml](meta/main.yml).

La versión de vagrant que se instala es la que se especifique en el fichero [vars/main.yml](vars/main.yml). En el mismo fichero se pueden especificar las boxes que se deben descargar y migrar a KVM.

Etiquetas
---------

El módulo utiliza dos etiquetas:

  - **packages**: para las tareas de instalación de paquetes del sistema operativo.
  - **vagrant**: para la instalación de vagrant y sus plugins.a
  - **vmx**: Crea la red virtual de gestión fuera de banda para los routers del [servicio gns3](../gns3/README.md)
