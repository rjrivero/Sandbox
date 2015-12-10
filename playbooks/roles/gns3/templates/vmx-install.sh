#!/usr/bin/env bash
#
# Must run as SUDO

cd "/opt/vmx/vmx-{{ vmx_version }}" || exit -1

{% for item in vmx_instances %}
if [ ! -d "build/{{ item.name }}" ]; then
    ./vmx.sh -lv --install --cfg "config/vmx-{{ item.name }}.conf"
    sleep 600
fi

{% endfor %}
