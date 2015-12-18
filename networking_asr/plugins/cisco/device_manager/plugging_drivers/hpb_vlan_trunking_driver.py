# Copyright 2014 Cisco Systems, Inc.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import time
from oslo_log import log as logging
from oslo_utils import excutils

from neutron.common import constants as l3_constants
from neutron.extensions import providernet as pr_net
from neutron.i18n import _LE
from neutron import manager

from networking_cisco.plugins.cisco,common import cisco_constants
from networking_cisco.plugins.cisco.device_manager import config
import networking_cisco.plugins.cisco.device_manager.plugging_drivers as plug


LOG = logging.getLogger(__name__)


class HBPVLANTrunkingPlugDriver(plug.hw_vlan_trunking_driver.HwVLANTrunkingPlugDriver):

    def allocate_hosting_port(self, context, router_id, port_db, network_type,
                              hosting_device_id):

        LOG.info("****************** allocate_hosting_port *****************")
        LOG.info("**************************** Allocating port {}".format(port_db['id']))

        dev_mgr = manager.NeutronManager.get_service_plugins().get(cisco_constants.DEVICE_MANAGER)
        asr_hd = dev_mgr.get_hosting_device(context, hosting_device_id)
        # I assume here that the ASR1k device in question has been registered
        # as a hosting_device with the name that the ML2 ACI mech driver uses
        # for that device.
        asr_host_name = asr_hd['name']
        self._core_plugin.update_port(context, port_db.id, {'port': {'binding:host_id': asr_host_name}})

        port_context = self._core_plugin.get_bound_port_context(context,port_db['id'])
        LOG.info(port_context)
        segment =  port_context.bottom_bound_segment

        allocated_vlan = None
        if segment:
            allocated_vlan =  segment["segmentation_id"]

        if allocated_vlan is not None:
            return {'allocated_port_id': port_db.id,
                    'allocated_vlan': allocated_vlan}

        # Database must have been messed up if this happens ...
        LOG.debug('hw_vlan_trunking_driver: Could not allocate VLAN')
        return


