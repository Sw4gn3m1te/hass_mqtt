from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pythoncom


def set_volume(volume_level):

    if not 0 <= volume_level <= 100:
        return "E"
    pythoncom.CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    volume.SetMasterVolumeLevelScalar(float(volume_level/100), None)


def get_volume():

    pythoncom.CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    current_volume = int(round(current_volume, 3)*100)
    return current_volume


if __name__ == '__main__':
    set_volume(39)
    print(get_volume())
