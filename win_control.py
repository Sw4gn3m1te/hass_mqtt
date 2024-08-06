from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pythoncom
import os
from pynput.keyboard import Controller, Key


class WinController:

    special_keys = {"shift": Key.shift, "alt": Key.alt, "ctrl": Key.ctrl, "altgr": Key.alt_gr, "capslock": Key.caps_lock,
                    "space": Key.space, "tab": Key.tab, "backspace": Key.backspace, "enter": Key.enter, "esc": Key.esc,
                    "arrowup": Key.up, "arrowdown": Key.down, "arrowleft": Key.left, "arrowright": Key.right}

    def __init__(self):
        self.shutdown_active = False
        self.ctrl = False
        self.shift = False
        self.capslock = False
        self.alt = False
        self.altgr = False

    @staticmethod
    def set_volume(volume_level):
        if not 0 <= volume_level <= 100:
            return "E"
        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        volume.SetMasterVolumeLevelScalar(float(volume_level / 100), None)

    @staticmethod
    def get_volume():

        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_volume = volume.GetMasterVolumeLevelScalar()
        current_volume = int(round(current_volume, 3)*100)
        return current_volume

    def shutdown(self):
        if not self.shutdown_active:
            os.system("shutdown /s /t 60")
            self.shutdown_active = True
        else:
            os.system("shutdown /a")
            self.shutdown_active = False

    def press_key(self, key):

        keyboard = Controller()

        if key in ["ctrl", "alt", "altgr", "shift", "capslock"]:
            if not self.__dict__[key]:
                self.__dict__[key] = True
                keyboard.press(WinController.special_keys[key])
            else:
                keyboard.release(WinController.special_keys[key])
                self.__dict__[key] = False

        elif key in ["space", "tab", "backspace", "enter", "arrowup", "arrowdown", "arrowleft", "arrowright", "esc"]:
            key = WinController.special_keys[key]
            keyboard.release(key)
            keyboard.press(key)

        else:
            keyboard.release(key)
            keyboard.press(key)
