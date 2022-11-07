#!/usr/bin/env python3
import glob
import logging
import os
import shutil
import subprocess
import time
import winreg

from AppException import AppException
from window_handler import window_handler
from win_app import win_app


class auto_fill_app():
    def __init__(self, opts: dict):
        self._opts = opts
        self._auto_info = self._opts.get("autoFillInfo")
        self._auto_login_action = self._get_login_action
        self._postrun = self._get_postrun
        self._proc = None
        self._win_app = None

    @property
    def _get_login_action(self) -> list:
        if not self._auto_info:
            return None
        return self._auto_info.get("action")

    @property
    def _get_postrun(self) -> list:
        postrun = self._opts.get("postRun")
        return postrun

    def _run_app(self) -> int:
        cmd_line = [self._opts["path"]]
        if "param" in self._opts:
            cmd_line += self._opts["param"].split()
        self._proc = subprocess.Popen(cmd_line)
        return self._proc.pid

    def _get_start_timeout(self):
        return self._opts["timeout"] if "timeout" in self._opts else 10

    def _start_app(self) -> win_app:
        pid = self._run_app()
        if pid < 0:
            raise AppException("Start app failed with pid = -1")
        logging.debug("Start app success, pid = %d" % (pid))
        t = 0
        interval = 2
        while t < self._get_start_timeout() / interval:
            app = win_app(pid)
            if self._auto_info and self._auto_info.get("title"):
                target = {"text": self._auto_info["title"]}
                if app.find_target_windows(**target):
                    return app
            elif app.handler:
                return app
            window_handler.dump_all_windows()
            time.sleep(interval)
            t += 1
        return None

    def exec_action(self, action: dict) -> bool:
        event = action.get("event")
        params = action.get("param")
        if not params:
            params = []
        if action.get("focus") == True:
            logging.debug("Set foreground again......")
            self._win_app.handler().set_foreground()
        target_hwnd = self._win_app.find_target_windows(**action["target"])
        if target_hwnd:
            logging.debug("Post event %s to %s" % (event, str(target_hwnd)))
            return target_hwnd.exec_action(event, *params)
        else:
            if action.get("continue") == True:
                return True
            return False

    def exec_fileclean(self, *args):
        for f in args:
            for real_file in glob.glob(os.path.expandvars(f)):
                if os.path.exists(real_file):
                    if os.path.isdir(real_file):
                        shutil.rmtree(real_file)
                    else:
                        os.unlink(real_file)

    def exec_command(self, *args):
        try:
            subprocess.Popen(list(args))
        except:
            pass

    @staticmethod
    def _del_reg_key(key):
        try:
            keylist = key.split('\\')
            HKEY = getattr(winreg, keylist[0])
            subkey = "\\".join(keylist[1:])
            with winreg.OpenKey(HKEY, subkey, access=winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_32KEY) as handler:
                index = 0
                while True:
                    try:
                        child_key = key + "\\" + winreg.EnumKey(handler, index)
                        auto_fill_app._del_reg_key(child_key)
                        index += 1
                    except OSError as e:
                        break
                try:
                    winreg.DeleteKey(handler, subkey)
                except:
                    winreg.DeleteKey(HKEY, subkey)
        except BaseException as e:
            logging.warn("Fail to delete key %s:%s " % (key, str(e)))

    def exec_regclean(self, *args):
        for key in args:
            auto_fill_app._del_reg_key(key)

    def _postrun_action(self, action: dict):
        exec = action.get("action")
        try:
            func = getattr(self, "exec_" + exec)
            if func:
                func(*action.get("params"))
        except Exception as e:
            logging.warn("exec action %s %s failed:%s" % (exec, action.get("params"), str(e)))

    def auto_login(self):
        if not self._auto_info or not self._auto_login_action:
            return True
        self._win_app.handler().set_foreground()
        if self._opts.get("maximize"):
            self._win_app.handler().set_maximize()
        step = 1
        for action in self._auto_login_action:
            logging.debug("=" * 20 + "begin" + "=" * 20)
            logging.debug("before exec action %s" % (str(action)))
            if not self.exec_action(action):
                # raise AppException("Auto fill action failed at step %d" % (step))
                logging.error("Auto fill action failed at step %d" % (step))
                return False
            if "wait" in action:
                time.sleep(action["wait"])
            logging.debug("After exec action %s" % (str(action)))
            logging.debug("=" * 20 + "end" + "=" * 20)
            self._win_app.dump_child_windows()
            logging.debug("=" * 20 + "end" + "=" * 20)
            logging.debug("\n\n")

            step += 1

        return True

    def start_app(self):
        # logging.debug("Start app, opts %s" % (str(self._opts)))
        self.postrun()
        self._win_app = self._start_app()
        if not self._win_app or not self._win_app.handler() and self._auto_login_action:
            # raise AppException("Start app %s failed" % (self._opts.get("path")))
            logging.error("Start app %s failed" % (self._opts.get("path")))
            return False

        return True

    def postrun(self):
        if not self._postrun:
            return
        for action in self._postrun:
            logging.debug("post run %s" % (str(action)))
            self._postrun_action(action)

    def join_app(self) -> bool:
        ret = True
        if self._proc:
            pid = self._proc.pid
            exit_value = self._proc.wait()
            logging.info("Proc %d exits with code %d" % (pid, exit_value))
            ret = ret and (exit_value == 0)
        logging.info("Exec post run for %s" % (self._opts.get("name")))
        self.postrun()
        return ret
