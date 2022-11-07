#!/usr/bin/env python3
import re
import sys
import logging

from window_handler import window_handler


class win_app(object):
    '''
    TODO: pid is fixed, maybe -1 mean all windows
    '''

    def __init__(self, pid: int):
        self._pid = pid
        self._hwnds = []
        self.get_window_handler()

    def get_window_handler(self):
        hwnds = window_handler.find_window_by_pid(self._pid)
        if hwnds:
            self._hwnds = [ hwnd for hwnd in hwnds if hwnd.is_normal()]

    def _get_default(self, key, default=None, **kwarg):
        return kwarg[key] if key in kwarg else default

    def _get_child_windows(self, hwnd: window_handler, hwnd_list: list = None) -> list:
        if not hwnd_list:
            hwnd_list = []
        if not hwnd in hwnd_list:
            hwnd_list.append(hwnd)
        child_hwnd_list = hwnd.get_child_windows()
        if not child_hwnd_list:
            return hwnd_list
        for child_hwnd in child_hwnd_list:
            self._get_child_windows(child_hwnd, hwnd_list)
        return hwnd_list

    def handler(self) -> window_handler:
        if self._hwnds:
            return self._hwnds[0]
        else:
            return None

    def dump_child_windows(self) -> list:
        hwnds = set()
        for hwnd in self._hwnds:
            if hwnd.is_normal():
                childs = self._get_child_windows(hwnd)
                if childs:
                    hwnds.update(childs)
        # hwnds = self._get_child_windows(self._hwnds[0])
        if not hwnds:
            return None
        logging.debug("dump all child window info")
        sorted_hwnds = sorted(list(hwnds))
        for h in sorted_hwnds:
            logging.debug(h)
        return sorted_hwnds

    def find_target_windows(self, **kwargs) -> window_handler:
        self.get_window_handler()
        logging.debug("find windows %s(pid %d, hwnd %s) target %s" % (self, self._pid, self._hwnds, str(kwargs)))
        if not self._hwnds:
            return None
        if not kwargs:
            hwnds = [hwnd for hwnd in self._hwnds if hwnd.is_normal()]
            return hwnds[0] if hwnds else None
        clazz = self._get_default("class", **kwargs)
        text = self._get_default("text", **kwargs)
        id = self._get_default("id", -1, **kwargs)
        seq = self._get_default("seq", 0, **kwargs)
        hwnds = self.dump_child_windows()

        try:
            if clazz:
                hwnds = [hwnd for hwnd in hwnds if re.search(clazz, hwnd.get_info().get("class"))]
            if id > 0:
                hwnds = [hwnd for hwnd in hwnds if hwnd.get_info().get("ctrlid") == id]
            if text:
                hwnds = [hwnd for hwnd in hwnds if re.search(text, hwnd.get_info().get("text"))]
            if hwnds:
                if seq < len(hwnds):
                    return hwnds[seq]
                else:
                    return None
            else:
                return None
        except:
            return None


if __name__ == "__main__":
    hwnds = window_handler.find_window_by_title("Navicat")
    if hwnds:
        pid = hwnds[0].get_pid()
    else:
        sys.exit(-1)
    app = win_app(pid)
    hwnd = app.find_target_windows(**{"text": "Navicat"})
    logging.debug(hwnd)
