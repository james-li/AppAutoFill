# /usr/bin/env python3
import logging
import time, re, ctypes
import os, sys, subprocess, win32gui, win32con, win32api, win32process
import glob, time

# Giant dictonary to hold key name and VK value
VK_CODE = {'backspace': 0x08,
           'tab': 0x09,
           'clear': 0x0C,
           'enter': 0x0D,
           'shift': 0x10,
           'ctrl': 0x11,
           'alt': 0x12,
           'pause': 0x13,
           'caps_lock': 0x14,
           'esc': 0x1B,
           'spacebar': 0x20,
           'page_up': 0x21,
           'page_down': 0x22,
           'end': 0x23,
           'home': 0x24,
           'left_arrow': 0x25,
           'up_arrow': 0x26,
           'right_arrow': 0x27,
           'down_arrow': 0x28,
           'select': 0x29,
           'print': 0x2A,
           'execute': 0x2B,
           'print_screen': 0x2C,
           'ins': 0x2D,
           'del': 0x2E,
           'help': 0x2F,
           '0': 0x30,
           '1': 0x31,
           '2': 0x32,
           '3': 0x33,
           '4': 0x34,
           '5': 0x35,
           '6': 0x36,
           '7': 0x37,
           '8': 0x38,
           '9': 0x39,
           'a': 0x41,
           'b': 0x42,
           'c': 0x43,
           'd': 0x44,
           'e': 0x45,
           'f': 0x46,
           'g': 0x47,
           'h': 0x48,
           'i': 0x49,
           'j': 0x4A,
           'k': 0x4B,
           'l': 0x4C,
           'm': 0x4D,
           'n': 0x4E,
           'o': 0x4F,
           'p': 0x50,
           'q': 0x51,
           'r': 0x52,
           's': 0x53,
           't': 0x54,
           'u': 0x55,
           'v': 0x56,
           'w': 0x57,
           'x': 0x58,
           'y': 0x59,
           'z': 0x5A,
           'numpad_0': 0x60,
           'numpad_1': 0x61,
           'numpad_2': 0x62,
           'numpad_3': 0x63,
           'numpad_4': 0x64,
           'numpad_5': 0x65,
           'numpad_6': 0x66,
           'numpad_7': 0x67,
           'numpad_8': 0x68,
           'numpad_9': 0x69,
           'multiply_key': 0x6A,
           'add_key': 0x6B,
           'separator_key': 0x6C,
           'subtract_key': 0x6D,
           'decimal_key': 0x6E,
           'divide_key': 0x6F,
           'F1': 0x70,
           'F2': 0x71,
           'F3': 0x72,
           'F4': 0x73,
           'F5': 0x74,
           'F6': 0x75,
           'F7': 0x76,
           'F8': 0x77,
           'F9': 0x78,
           'F10': 0x79,
           'F11': 0x7A,
           'F12': 0x7B,
           'F13': 0x7C,
           'F14': 0x7D,
           'F15': 0x7E,
           'F16': 0x7F,
           'F17': 0x80,
           'F18': 0x81,
           'F19': 0x82,
           'F20': 0x83,
           'F21': 0x84,
           'F22': 0x85,
           'F23': 0x86,
           'F24': 0x87,
           'num_lock': 0x90,
           'scroll_lock': 0x91,
           'left_shift': 0xA0,
           'right_shift ': 0xA1,
           'left_control': 0xA2,
           'right_control': 0xA3,
           'left_menu': 0xA4,
           'right_menu': 0xA5,
           'browser_back': 0xA6,
           'browser_forward': 0xA7,
           'browser_refresh': 0xA8,
           'browser_stop': 0xA9,
           'browser_search': 0xAA,
           'browser_favorites': 0xAB,
           'browser_start_and_home': 0xAC,
           'volume_mute': 0xAD,
           'volume_Down': 0xAE,
           'volume_up': 0xAF,
           'next_track': 0xB0,
           'previous_track': 0xB1,
           'stop_media': 0xB2,
           'play/pause_media': 0xB3,
           'start_mail': 0xB4,
           'select_media': 0xB5,
           'start_application_1': 0xB6,
           'start_application_2': 0xB7,
           'attn_key': 0xF6,
           'crsel_key': 0xF7,
           'exsel_key': 0xF8,
           'play_key': 0xFA,
           'zoom_key': 0xFB,
           'clear_key': 0xFE,
           '+': 0xBB,
           ',': 0xBC,
           '-': 0xBD,
           '.': 0xBE,
           '/': 0xBF,
           '`': 0xC0,
           ';': 0xBA,
           '[': 0xDB,
           '\\': 0xDC,
           ']': 0xDD,
           "'": 0xDE,
           '`': 0xC0}


class window_handler(object):
    def __init__(self, hwnd):
        self._hwnd = hwnd
        self.refresh_info()
        self._action = {
            "mouse": self.click_mouse,
            "keyboard": self.input_key,
            "message": self.send_message,
            "hide": self.hide_target
        }

    def __str__(self):
        return "%d:%s:%s:%d:%s ->%s" % (
            self._info['pid'], hex(self._hwnd), self._info["class"], self._info["ctrlid"], self._info["text"],
            str(self._info["rect"]))

    def is_normal(self):
        return window_handler.is_normal_window(self._hwnd)

    def __hash__(self):
        return self._hwnd

    def get_rect(self):
        return self._info.get("rect", (0,0,0,0))

    def __lt__(self, other):
        if type(other) != window_handler:
            raise ValueError
        my_rect = self.get_rect()
        other_rect = other.get_rect()
        return my_rect < other_rect


    @staticmethod
    def enum_window(filter_func=None):
        if not filter_func:
            filter_func = window_handler.is_normal_window

        def __enum_window_handler(hwnd, hwnd_list):
            # if window_handler.is_normal_window(hwnd) and (not filter_func or filter_func(hwnd)):
            if filter_func(hwnd):
                hwnd_list.append(window_handler(hwnd))

        hwnd_list = []
        win32gui.EnumWindows(__enum_window_handler, hwnd_list)
        return hwnd_list

    @staticmethod
    def dump_all_windows(**kwargs):
        hwnd_list = []
        try:
            if kwargs:
                if kwargs.get("pid"):
                    hwnd_list = window_handler.find_window_by_pid(kwargs.get("pid"))
                elif kwargs.get("title"):
                    hwnd_list = window_handler.find_window_by_title(kwargs.get('title'))
            else:
                hwnd_list = window_handler.enum_window()
            for hwnd in hwnd_list:
                info = "%d:%d:%s:%s" % (window_handler.get_window_pid(hwnd.get_hwnd()),
                                        hwnd.get_hwnd(),
                                        window_handler.get_window_class(hwnd.get_hwnd()),
                                        window_handler.get_window_text(hwnd.get_hwnd()))
                try:
                    logging.debug(info)
                except:
                    pass
        except:
            pass

    @staticmethod
    def get_window_pid(hwnd):
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            return pid
        except BaseException as e:
            return -1

    @staticmethod
    def is_normal_window(hwnd):
        try:
            return win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd)
        except:
            return False

    @staticmethod
    def get_window_class(hwnd):
        try:
            return win32gui.GetClassName(hwnd)
        except:
            return None

    @staticmethod
    def get_window_text(hwnd):
        title = win32gui.GetWindowText(hwnd)
        return title

    @staticmethod
    def get_window_rect(hwnd):
        try:
            return win32gui.GetWindowRect(hwnd)
        except:
            return (0,0,0,0)

    @staticmethod
    def get_window_ctrlid(hwnd):
        return win32gui.GetDlgCtrlID(hwnd)

    @staticmethod
    def find_window_by_pid(pid: int) -> list:
        def pid_matched(hwnd):
            try:
                wpid = window_handler.get_window_pid(hwnd)
                # logging.debug("search hwnd(%s, %d) for pid (%d)"%(hwnd, wpid, pid))
                return wpid == pid
            except:
                return False

        return window_handler.enum_window(pid_matched)

    @staticmethod
    def find_window_by_title(title: str) -> list:
        def title_matched(hwnd):
            try:
                return window_handler.get_window_text(hwnd).startswith(title)
            except:
                return False

        return window_handler.enum_window(title_matched)

    def get_hwnd(self):
        return self._hwnd

    def get_info(self):
        return self._info

    @staticmethod
    def enum_child_window(hwnd: int):
        def __enum_child_handler(h, hwnd_list):
            hwnd_list.append(h)
            return True

        hwnds = []
        try:
            win32gui.EnumChildWindows(hwnd, __enum_child_handler, hwnds)
        except BaseException as e:
            pass
        return hwnds

    def get_hwnd_info(self) -> dict:
        info = {}
        info["pid"] = window_handler.get_window_pid(self._hwnd)
        info["class"] = window_handler.get_window_class(self._hwnd)
        info["text"] = window_handler.get_window_text(self._hwnd)
        info["ctrlid"] = window_handler.get_window_ctrlid(self._hwnd)
        child_list = window_handler.enum_child_window(self._hwnd)
        info["child"] = [window_handler(x) for x in child_list]
        info["rect"] = window_handler.get_window_rect(self._hwnd)
        return info

    def get_child_windows(self) -> list:
        if "child" not in self._info:
            self.refresh_info()
        return self._info["child"]

    def get_pid(self):
        if "pid" not in self._info:
            self.refresh_info()
        return self._info["pid"]

    def refresh_info(self):
        self._info = self.get_hwnd_info()

    def move_mouse(self, point):
        if "rect" in self._info:
            point = (point[0] + self._info["rect"][0], point[1] + self._info["rect"][1])
        logging.debug("Move mouse to (%d,%d)" % (point[0], point[1]))
        win32api.SetCursorPos(point)

    def click_mouse(self, point, button=None):
        self.move_mouse(point)
        time.sleep(0.05)
        if not button:
            return True
        button = button.upper()
        down_msg, up_msg = win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP
        if button == "RIGHT":
            down_msg, up_msg = win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP

        win32api.mouse_event(down_msg, 0, 0, 0, 0)
        win32api.mouse_event(up_msg, 0, 0, 0, 0)
        if button == "DOUBLE_CLICK":
            win32api.mouse_event(down_msg, 0, 0, 0, 0)
            win32api.mouse_event(up_msg, 0, 0, 0, 0)
        logging.debug("Click mouse with button %s" % button)
        return True

    @staticmethod
    def _strcasecmp(s1: str, s2: str):
        if s1 and s2:
            return s1.lower() == s2.lower()
        elif s1 or s2:
            return False
        else:
            return True

    def input_key(self, point, words, function_key=None):
        if "rect" in self._info and (point[0] + point[1]) > 0:
            self.click_mouse(point, "LEFT")
            time.sleep(0.5)
        for word in words:
            shift = False
            if function_key:
                self._function_key_press(function_key)
            if ord(word) in range(ord('A'), ord('Z') + 1):
                shift = True
                win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
                word = word.lower()
            win32api.keybd_event(VK_CODE[word], 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(VK_CODE[word], 0, win32con.KEYEVENTF_KEYUP, 0)
            if shift:
                win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
            if function_key:
                self._function_key_press(function_key, False)
        logging.debug("Input key %s" % words)
        return True

    def send_message(self, message, params=None):
        try:
            msg_id = getattr(win32con, message)
            win32api.SendMessage(self._hwnd, msg_id, 0, params)
            return True
        except AttributeError as e:
            pass
        return False

    def set_text(self, text):
        self.send_message("WM_SETTEXT", text)

    def hide_target(self, hide):
        try:
            if hide:
                win32gui.ShowWindow(self._hwnd, win32con.SW_HIDE)
            else:
                win32gui.ShowWindow(self._hwnd, win32con.SW_SHOW)
        except:
            pass
        return True

    def exec_action(self, action, *args):
        if action in self._action:
            func = self._action[action]
            return func(*args)
        else:
            return True

    def set_foreground(self):
        try:
            win32gui.SetForegroundWindow(self._hwnd)
        except:
            pass

    def set_maximize(self):
        try:
            win32gui.ShowWindow(self._hwnd, win32con.SW_MAXIMIZE)
        except:
            pass

    def __eq__(self, others):
        if not isinstance(others, self.__class__):
            return False
        if others._hwnd == self._hwnd:
            return True
        return False

    def _function_key_press(self, function_key, press=True):
        if self._strcasecmp(function_key, "ctrl"):
            win32api.keybd_event(VK_CODE['left_control'], 0, win32con.KEYEVENTF_KEYUP if not press else 0, 0)
        elif self._strcasecmp(function_key, "alt"):
            win32api.keybd_event(VK_CODE['left_alt'], 0, win32con.KEYEVENTF_KEYUP if not press else 0, 0)
