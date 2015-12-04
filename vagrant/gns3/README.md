Vagrantfile de servidor GNS3
============================

Este [Vagrantfile](Vagrantfile) crea un servidor GNS3 con 2 vCPUS, 12 gigas de RAM, una conexión a la red de gestión **192.168.199.10**, y varias instancias preconfiguradas de [Juniper vMX](http://www.juniper.net/us/en/products-services/routing/mx-series/vmx/).

El Vagrantfile sólo se encarga de la asignación de recursos a la máquina virtual: memoria, número de vCPUs, y red. Para todas las configuraciones del servicio, hay que consultar el [rol gns3](../../playbooks/roles/gns3/README.md) de Ansible.

Para crear el entorno GNS3, basta con ejecutar:

```
vagrant --provider=kvm up
```
