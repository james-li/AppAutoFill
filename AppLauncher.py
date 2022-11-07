#!/usr/bin/env python3
import json
import sys
import traceback

import requests
import logging
import os

from AppException import AppException
from auto_fill_app import auto_fill_app


def callback(url, **args):
    callback_url = url
    if not callback_url:
        return
    try:
        requests.get(callback_url, params=args, timeout=10)
    except Exception:
        pass


def app_launch(url):
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError as e:
        # traceback.print_exc()
        logging.error('Connect failed:%s' % (str(e)))
        return
    if not response:
        return
    ret = True
    msg = ""
    app_info = dict()
    app = None
    try:
        app_info = json.loads(response.text)
        logging.debug('AppLauncher: exec "%s"' % (app_info.get("path")))
        app = auto_fill_app(app_info)
        if not app:
            raise AppException("Initialize auto fill app failed")

        _ret = app.start_app()
        callback(app_info.get("callback"), **{"launchSuccess": _ret})
        if not _ret:
            return

        _ret = app.auto_login()
        callback(app_info.get("callback"), **{"appReady": _ret})
        if not _ret:
            return

    except BaseException as e:
        # traceback.print_exc()
        logging.error("AppLauncher failed: %s" % (traceback.format_exc()))
        msg = "exec app failed: " + str(e)
        ret = False
    if not app:
        sys.exit(-1)
    callback(app_info.get("callback"), **{"success": str(ret).lower(), "msg": msg})
    app.join_app()
    callback(app_info.get("callback"), **{"sessionClose": str(ret)})


if __name__ == "__main__":
    EXECDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    LOGDIR = os.path.join(EXECDIR, "logs")
    try:
        if not os.path.exists(LOGDIR):
            os.mkdir(LOGDIR)
        log_level = logging.INFO
        if os.environ.get("APPLAUNCHER_DEBUG"):
            log_level = logging.DEBUG

        logging.basicConfig(
            handlers=[logging.FileHandler(encoding='utf-8', mode='a', filename=os.path.join(LOGDIR, "log.txt"))],
            format="%(asctime)s %(levelname)s:%(message)s",
            level=log_level)
        if os.environ.get("APPLAUNCHER_DEBUG"):
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    except:
        traceback.print_exc()
        pass
    if len(sys.argv) > 1:
        app_launch(sys.argv[1])
