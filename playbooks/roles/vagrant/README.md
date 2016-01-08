Rol de servidor Vagrant
=======================

Este rol instala el paquete vagrant de https://www.vagrantup.com/. Junto con vagrant, se instalan los plugins:

  - [vagrant-libvirt](https://github.com/pradels/vagrant-libvirt), para poder ejecutar maquinas virtuales con KVM en lugar de VirtualBox.
  - [vagrant-mutate](https://github.com/sciurus/vagrant-mutate), para convertir boxes de VirtualBox a formato KVM.

Además, crea una red de administración **vMX_mgmt** para poder compartir un espacio de direcciones entre libvirt y docker. Los contenedores Docker usaran esta red como red interna, y las maquinas creadas con libvirt podran tener una interfaz en esta red para comunicarse con los contenedores.

Configuracion
-------------

El rol hereda de [KVM](../kvm/README.md), que le permite especificar el tamaño y la ruta del espacio de swap en el fichero [meta/main.yml](meta/main.yml).

La versión de vagrant que se instala es la que se especifique en el fichero [vars/main.yml](vars/main.yml). En el mismo fichero se pueden especificar las boxes que se deben descargar y migrar a KVM.

Etiquetas
---------

El módulo utiliza las siguientes etiquetas:

  - **packages**: para las tareas de instalación de paquetes del sistema operativo.
  - **vagrant**: para la instalación de vagrant y sus plugins.
  - **network**: Crea la red virtual interna para la integración con docker. 

Para permitir que las instancias creadas con vagrant y los contenedores docker se comuniquen, se usa como bridge para docker una red virtual creada con libvirt.

  - Por motivos historicos, esta red se llama **vMX_mgmt** y tiene el direccionamiento **192.168.199.0/24**.
  - El [rol docker](../docker/README.yml) configura el sistema para que docker use esta misma red para los contenedores.
  - De esta forma, las maquinas virtuales y los contenedores pueden comunicarse internamente por esa red.
