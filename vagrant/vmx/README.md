Vagrantfile de servidor VMX
===========================

Este [Vagrantfile](Vagrantfile) crea un servidor VMX con una conexión a la red de gestión **192.168.199.10**, y varias instancias preconfiguradas de [Juniper vMX](http://www.juniper.net/us/en/products-services/routing/mx-series/vmx/).

El Vagrantfile sólo se encarga de la asignación de recursos a la máquina virtual: memoria, número de vCPUs, y red. Para todas las configuraciones del servicio, hay que consultar el [rol vmx](../../playbooks/roles/vmx/README.md) de Ansible.

Para crear el entorno VMX, basta con ejecutar:

```
vagrant --provider=kvm up
```
