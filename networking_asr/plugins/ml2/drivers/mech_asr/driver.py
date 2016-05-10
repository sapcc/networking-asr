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

from neutron.plugins.common import constants as p_constants


import constants



LOG = logging.getLogger(__name__)


cfg.CONF.import_group('ml2_asr',
                      'networking_asr.plugins.ml2.drivers.mech_asr.config')


class CiscoASRMechanismDriver(api.MechanismDriver):
    def __init__(self):
        LOG.info(_LI("ASR mechanism driver initializing..."))

        self.vif_type = constants.VIF_TYPE_ASR
        self.vif_details = {portbindings.CAP_PORT_FILTER: False}
        self.physical_networks = cfg.CONF.ml2_asr.physical_networks

        super(CiscoASRMechanismDriver, self).__init__()

        LOG.info(_LI("ASR mechanism driver initialized."))

    def initialize(self):
        pass

    def bind_port(self, context):
        device_owner = context.current['device_owner']
        if device_owner and device_owner.startswith('network:router'):
            # bind to first segment if no physical networks are configured
            if self.physical_networks is None:
                self._set_binding(context, context.segments_to_bind[0])
                return True


            for segment in context.segments_to_bind:
                if segment[api.PHYSICAL_NETWORK] in self.physical_networks:
                    self._set_binding(context, segment)

                    LOG.debug("Set binding for port %(port)s for physical network %(physical_network)s", {'port':str(context.current[api.ID]), 'physical_network': str(segment[api.PHYSICAL_NETWORK])})

                    return True

            LOG.error("No segment matches the configured physical networks "
                      "%(physical_networks)s",
                      {'physical_networks': self.physical_networks})
        return False

    def _set_binding(self, context, segment):
        context.set_binding(segment[api.ID],
                            self.vif_type,
                            self.vif_details,
                            p_constants.ACTIVE)



