import platform
import winreg
from unittest import TestCase

from auto_fill_app import auto_fill_app


class TestAuto_fill_app(TestCase):
    def test__del_reg_key(self):
        key = r"HKEY_CURRENT_USER\Software\PremiumSoft\Navicat\Servers\test"
        auto_fill_app._del_reg_key(key)
