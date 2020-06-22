import clr
import ctypes
import numpy as np

clr.FindAssembly("OlympusNDT.Instrumentation.NET.dll")
clr.AddReference('OlympusNDT.Instrumentation.NET')

from OlympusNDT.Instrumentation.NET import Utilities, IDeviceDiscovery, DiscoverResult, IFirmwarePackageScanner
from OlympusNDT.Instrumentation.NET import UltrasoundTechnology, IAcquisition


class FPXDevice(object):
    def __init__(self, ip_address):
        Utilities.ResolveDependenciesPath()
        deviceDiscovery = IDeviceDiscovery.Create(ip_address)
        discoverResult = deviceDiscovery.DiscoverFor(5000)
        self.device = discoverResult.device
        if discoverResult.status == DiscoverResult.Status.DeviceFound:
            print("Focus PX Device is found!")

    def download_firmware_package(self, package_name):
        firmwarePackages = IFirmwarePackageScanner.GetFirmwarePackageCollection()
        for i in range(firmwarePackages.GetCount()):
            fw_name = firmwarePackages.GetFirmwarePackage(i).GetName()
            if fw_name.find(package_name) != -1:
                print("Firmware Package %s is found!" % fw_name)
                firmwarePackage = firmwarePackages.GetFirmwarePackage(i)
                self.device.Start(firmwarePackage)
                print("Firmware Package is started!")
                return

    def create_beamset(self, connector_index):
        deviceConfiguration = self.device.GetConfiguration()
        ultrasoundConfiguration = deviceConfiguration.GetUltrasoundConfiguration()
        digitizerTechnology = ultrasoundConfiguration.GetDigitizerTechnology(UltrasoundTechnology.Conventional)
        beamSetFactory = digitizerTechnology.GetBeamSetFactory()
        beamSet = beamSetFactory.CreateBeamSetConventional("Conventional")
        connector = digitizerTechnology.GetConnectorCollection().GetConnector(connector_index)
        ultrasoundConfiguration.GetFiringBeamSetCollection().Add(beamSet, connector)

    def init_acquisition(self):
        self.acquisition = IAcquisition.CreateEx(self.device)

    def collect_ascan(self):
        result = self.acquisition.WaitForDataEx()
        if result.status == IAcquisition.WaitForDataResultEx.Status.DataAvailable:
            ascan = result.cycleData.GetAscanCollection().GetAscan(0)
            ascan_ptr = ascan.GetData()
            sample_quantity = ascan.GetSampleQuantity()
            print("sample_quantity: %d" % sample_quantity)
            print(type(ascan_ptr))
            print(ascan_ptr)
            print(ascan_ptr.ToInt64())
            # use numpy
            newpnt = ctypes.cast(ascan_ptr.ToInt64(), ctypes.POINTER(ctypes.c_int32))
            DataBytes = np.ctypeslib.as_array(newpnt, (sample_quantity,))  # no internal copy
            print(type(DataBytes))
            print(DataBytes.tolist().__len__())
            print(DataBytes.tolist())


if __name__ == '__main__':
    ip_address = "192.168.0.1"
    fpx = FPXDevice(ip_address)
    package_name = "FocusPxPackage-1.3"
    fpx.download_firmware_package(package_name)
    fpx.create_beamset(4)
    fpx.init_acquisition()
    fpx.acquisition.ApplyConfiguration()
    fpx.acquisition.Start()
    fpx.collect_ascan()
    fpx.acquisition.Stop()
