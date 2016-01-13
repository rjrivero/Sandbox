Simulador de JunOS
==================

Este rol instala el simulador de JunOS Olive, y el fichero de configuracion de gns3 para poder usarlo.

Preparacion
-----------

La imagen del simulador de JunOs no esta incluida en el repositorio, por motivos legales y porque pesa un Giga. Si no la tienes, hay que crearla a mano siguiendo alguno de los tutoriales que hay online. A mi me ha funcionado [este](http://brezular.com/2012/07/03/installing-olive-12-1r1-9-under-qemu/) para la version 13.3R8 de JunOS.

Por si acaso el tutorial desaparece de la web, resumo aqui los pasos:

### Imagenes de software

  - Descargar [freebsd 4.11, imagen de miniinst](http://ftp-archive.freebsd.org/pub/FreeBSD-Archive/old-releases/i386/ISO-IMAGES/4.11/4.11-RELEASE-i386-miniinst.iso).
  - Descargar una imagen **domestic signed (US/Canada)** de JunOS para series M/T/MX
  - Crear un disco de arranque para FreeBSD con

```
qemu-img create -f qcow2 olive-base.img 16G
```

### Instalacion de FreeBSD

El instalador de FreeBSD se lanza con:

```
qemu-system-x86_64 -m 2G -hda olive-base.img -cdrom 4.11-RELEASE-i386-miniinst.iso -enable-kvm -net nic,macaddr=00:aa:00:60:01:01,model=e1000 -net user
```

Los pasos a usar en el instalador son:

  - Standard Installation
  - Create disk partitions

    - a - Use Entire Disk
    - Install a Standard MBR
    - c - Create new partitions

```
ad0s1a    /         4096M
ad0s1b    swap      4096M
ad0s1e    /config   256M
ad0s1f    /var      restante
```

  - Minimal Distribution Type
  - Install from a FreeBSD CD / VDD
  - Responder "No" al resto de preguntas del instalador.
  - Proporcionar un password para el usuario **root**.
  - Completar la instalacion y el reinicio.

### Tuneo del instalador JunOS

El siguiente paso es preparar el instalador de JunOS. Lo primero es extraer la utilidad **true** de la maquina FreeBSD, para poder usarla al crear la imagen del instalador. Desde el FreeBSD:

```
dhclient em0
```

Este comando asignara a la maquina una IP del rango 10.0.2.0/24. Usaremos esta red para copiar el programa **true** al host:

```
scp -rv /usr/bin/true <username>@10.0.2.2:/home/<username>
# Ya se puede apagar la maquina virtual
halt
```

Lo siquiente es desempaquetar el instalador y editarlo para permitir que pueda ejecutarse en un FreeBSD generico. Esto lo haremos desde el host:

```
mkdir jinst-signed
cd jinst-signed
tar -xzvf ../jinstall-13.3R8.7-domestic-signed.tgz

mkdir jinst
cd jinst
tar -xzvf ../jinstall-13.3R8.7-domestic.tgz

mkdir pkgtools
cd pkgtools
tar -xzvf ../pkgtools.tgz
```

Hay que copiar el ejecutable **true** que extrajimos de FreeBSD a la carpeta *pkgtools/bin*

```
rm         bin/checkpic
cp ~/true  bin/checkpic
chmod 0555 bin/checkpic

tar -czvf ../pkgtools.tgz *
cd ..
rm -rf pkgtools
```

Y hay que editar un par de ficheros para eliminar las referencias a hw.re.name:

```
sed 's/re_name=".*/re_name="olive"/' -- +INSTALL
sed 's/re_name=".*/re_name="olive"/' -- +REQUIRE
```

Y con eso, ya se puede volver a empaquetar el instalador y crear un ISO para facilitar el acceso desde la maquina virtual:

```
tar -czvf ~/jinstall-olive.tgz *
mkisofs -J -o ~/jinstall-olive.iso ~/jinstall-olive.tgz
```

### Instalacion del software JunOS

Volvemos a arrancar la maquina virtual, con el CDROM que hemos creado, y lanzamos el instalador.

```
qemu-system-x86_64 -m 2G -hda olive-base.img -cdrom ~/jinstall-olive.iso -enable-kvm

# Dentro de la maquina virtual
mount /cdrom

# Pulsar Enter dos veces
pkg_add -f /cdrom/jinstall-olive.tgz
# Paciencia!
```

Al terminar, sugerira reiniciar. No recomiendo hacerlo porque al reiniciar ya no utiliza la salida por consola, sino por puerto serie. Es mejor apagar la maquina (con halt) y volver a lanzarla redirigiendo el puerto:

```
qemu-system-x86_64 -m 2G -hda olive-base.img -enable-kvm -serial telnet:0.0.0.0:3000,server
```

Podemos hacer telnet a **localhost 3000** y ver el progreso del instalador. Una vez terminado, reiniciara y nos encontraremos con el login de **root**, sin password.

Configuracion
-------------

La imagen virtual que hayamos preparado por el procedimiento anterior tendremos que copiarla al directorio **files** del rol. A continuacion, habra que configurar el fichero [vars/main.yml](vars/main-yml), poniendo en la variable **junos_image** el nombre del fichero de imagen.

Core dump en Junos OS
---------------------

Tras completar la instalacion y empezar a usar la imagen, se detectara que la maquina virtual se reinicia ocasionalmente con el error:

```
ad1: Standby not armed but state is invalid: state="ARMED"
```

Para solucionarlo, hay que introducir en modo configuracion el **comando oculto**:

```
set chassis routing-engine disk no-standby
```

El origen del problema esta descrito en el articulo (http://kb.juniper.net/InfoCenter/index?page=content&id=KB29164&actp=RSS)
