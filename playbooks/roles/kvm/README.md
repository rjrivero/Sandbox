Rol KVM
=======

Este rol instala los paquetes de QEMU-KVM, habilita el soporte de HugePages, y crea un espacio de swap.

Opcionalmente, puede activar el cifrado en el equipo:

  - Utilizando cifrado con clave aleatoria para el swap, si se especifica la variable **swap_crypt: true**.
  - Montando un grupo de volumen (VG Volume Group) sobre un dispositivo cifrado que esté abierto con cryptsetup, si se especifica la variable **crypt_device**.

Configuración
-------------

El rol acepta los siguientes paŕametros:

  - swap_megas: Megabytes a provisionar para swap (por ejemplo, 8192 = 8 Gigas)
  - swap_path: Ruta al fichero de swap.
  - swap_crypt: (opcional): true para que el swap sea cifrado con una clave aleatoria.
  - apt_repos: (opcional): lista de repositorios apt a añadir antes de actualizar la cache de apt.
  - crypt_device (opcional): Dispositivo luks donde se crea el VG. El dispositivo debe haber sido ya abierto con cryptsetup.

```
sudo cryptsetup open <ruta al dispositivo> <crypt_device>
```

