import ctypes
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def set_volume(volume_level):
    """
    Sets the system volume to the specified level.

    :param volume_level: Volume level (float) between 0.0 and 1.0
    """
    if not 0.0 <= volume_level <= 1.0:
        raise ValueError("Volume level must be between 0.0 and 1.0")

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Set the volume level
    volume.SetMasterVolumeLevelScalar(volume_level, None)


# Example usage:
# Set the volume to 50%
set_volume(0.5)
