openstack-networking-asr
========================

Openstack L2 networking components for Cisco ASR L3 support


Install on devstack
-------------------

clone repo into /opt/stack

cd ./networking-asr

python setup.py install

add asr mechanism driver to /etc/neutron/plugins/ml2/ml2_conf.ini

restart neutron server

