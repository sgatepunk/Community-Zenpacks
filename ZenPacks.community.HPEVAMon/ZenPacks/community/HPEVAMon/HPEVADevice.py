################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVADevice

HPEVADevice is an abstraction of a HP EVA

$Id: HPEVADevice.py,v 1.1 2010/05/14 18:03:32 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenModel.Device import Device
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenModel.ZenStatus import ZenStatus
from ZenPacks.community.HPEVAMon.HPEVADeviceHW import HPEVADeviceHW
from ZenPacks.community.HPEVAMon.HPEVADeviceOS import HPEVADeviceOS
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class HPEVADevice(Device):

    def __init__(self, id, buildRelations=True):
        ManagedEntity.__init__(self, id, buildRelations=buildRelations)
        os = HPEVADeviceOS()
        self._setObject(os.id, os)
        hw = HPEVADeviceHW()
        self._setObject(hw.id, hw)
        self._lastPollSnmpUpTime = ZenStatus(0)
        self._snmpLastCollection = 0
        self._lastChange = 0
        self.buildRelations()

    factory_type_information = (
        {
            'immediate_view' : 'deviceStatus',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'deviceStatus'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'osdetail'
                , 'name'          : 'OS'
                , 'action'        : 'hpevaDeviceOsDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'hwdetail'
                , 'name'          : 'Hardware'
                , 'action'        : 'hpevaDeviceHardwareDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfServer'
                , 'name'          : 'Perf'
                , 'action'        : 'viewDevicePerformance'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'edit'
                , 'name'          : 'Edit'
                , 'action'        : 'editDevice'
                , 'permissions'   : ("Change Device",)
                },
            )
         },
        )

    def sysUpTime(self):
        upTime = -1
        for cntr in self.getDeviceComponents(type='HPEVAStorageProcessorCard'):
            cntrSysUpTime = cntr.sysUpTime()
            if cntrSysUpTime > upTime: upTime = cntrSysUpTime
        return upTime

InitializeClass(HPEVADevice)
