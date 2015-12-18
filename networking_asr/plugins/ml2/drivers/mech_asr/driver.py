# Copyright 2014 IBM Corp.
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

import netaddr

from neutron.extensions import portbindings
from oslo_config import cfg
from oslo_log import log as logging

from neutron.i18n import _LI
from neutron.i18n import _LW
from neutron.plugins.ml2 import driver_api as api

LOG = logging.getLogger(__name__)


class CiscoASRMechanismDriver(api.MechanismDriver):

    def __init__(self):
        LOG.info(_LI("ASR mechanism driver initializing..."))

        self.vif_type = "asr"
        self.vif_details = {portbindings.CAP_PORT_FILTER: False}




    def initialize(self):
        pass


    def bind_port(self, context):

        network_id = context.network.current['id']

        # For now we will just bind the last segment
        segment = context.segments_to_bind.pop()

        device_owner = context.current['device_owner']

        # For now use the simple check that its a network object,
        # needs refinement because this will include DHCP agents
        # Workaround now by putting asr driver at end of list in config
        if device_owner and device_owner.startswith('network'):
            context.set_binding(segment[api.ID], self.vif_type,self.vif_details)

        return True

