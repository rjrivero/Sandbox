#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import socket
import sys
import netifaces

from jinja2 import Environment, FileSystemLoader


def scan_ifaces(mgmt_iface, *network_ifaces):

    interfaces = netifaces.interfaces()

    # Get management MAC address and auto-calculate two more for vMX
    if not mgmt_iface in interfaces:
        return "ERROR: mgmt interface %s not found" % mgmt_iface
    mgmt_mac = netifaces.ifaddresses(mgmt_iface)[netifaces.AF_LINK][0]['addr']

    # Create additional MACs 1 and 2
    mac_bytes = mgmt_mac.split(':')
    pref_byte = ":".join(mac_bytes[:-1])
    last_byte = int("0x%s" % mac_bytes[-1], 16)
    mgmt_mac1 = "%s:%02x" % (pref_byte, last_byte + 1)
    mgmt_mac2 = "%s:%02x" % (pref_byte, last_byte + 2)

    # Get mgmt interface IPv4 address
    mgmt_ip = netifaces.ifaddresses(mgmt_iface)[netifaces.AF_INET][0]['addr']
    ipad_bytes = mgmt_ip.split('.')
    pref_byte = ".".join(ipad_bytes[:-1])
    last_byte = int(ipad_bytes[-1])
    mgmt_ip1  = "%s.%d" % (pref_byte, last_byte + 1)
    mgmt_ip2  = "%s.%d" % (pref_byte, last_byte + 2)

    # Get MAC addresses of data interfaces
    ifaces_mac = list()
    for iface in network_ifaces:
        if not iface in interfaces:
            return "ERROR: not existing interface %s" % iface
        if_mac = netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr']
        ifaces_mac.append(if_mac)

    # OOOK!
    return {
        'hostname'    : socket.gethostname(),
        'vmx_version' : "{{ vmx_version }}",
        'vfpc_version': "{{ vfpc_version }}",
        'mgmt_iface'  : mgmt_iface,
        'mgmt_mac'    : mgmt_mac,
        'mgmt_ip'     : mgmt_ip,
        'mgmt_mac1'   : mgmt_mac1,
        'mgmt_ip1'    : mgmt_ip1,
        'mgmt_mac2'   : mgmt_mac2,
        'mgmt_ip2'    : mgmt_ip2,
        'ifaces_mac'  : ifaces_mac,
        'ifaces_name' : tuple(network_ifaces)
    }

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print ("Modo de uso: %s [mgmt_iface] [access_ifaces...]" % sys.argv[0])
        sys.exit(-1)

    # Escanea las interfaces y construye el entorno para el template
    result = scan_ifaces(sys.argv[1], *sys.argv[2:])
    if isinstance(result, basestring):
        print (result)
        sys.exit(-2)

    # Vuelca el template en vmx.conf
    environ  = Environment(loader=FileSystemLoader("."))
    # vmx.conf template
    template = environ.get_template("vmx.conf.template")
    config   = template.render(result)
    with open("vmx.conf", "w+") as conf_file:
        conf_file.write(config)
    # vmx-junosdev.conf template
    template = environ.get_template("vmx-junosdev.conf.template")
    config   = template.render(result)
    with open("vmx-junosdev.conf", "w+") as conf_file:
        conf_file.write(config)
    # Success!
    print ("Success!")

