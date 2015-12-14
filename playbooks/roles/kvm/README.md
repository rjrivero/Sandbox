Rol KVM
=======

Este rol instala los paquetes de QEMU-KVM, habilita el soporte de HugePages, y crea un espacio de swap.

Configuración
-------------

El rol acepta los siguientes paŕametros:

  - swap_megas: Megabytes a provisionar para swap (por ejemplo, 8192 = 8 Gigas)
  - swap_path: Ruta al fichero de swap.
  - swap_crypt: (opcional): true para que el swap sea cifrado con una clave aleatoria.
  - apt_repos: (opcional): lista de repositorios apt a añadir antes de actualizar la cache de apt.

