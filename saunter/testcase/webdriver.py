import logging

from saunter.SeleniumWrapper import SeleniumWrapper as wrapper

import saunter.ConfigWrapper

if saunter.ConfigWrapper.ConfigWrapper().config.getboolean("SauceLabs", "ondemand"):
    import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from saunter.testcase.base import BaseTestCase

capabilities_map = {
    "firefox": DesiredCapabilities.FIREFOX,
    "iexplore": DesiredCapabilities.INTERNETEXPLORER
}

os_map = {
    "Windows 2003": "XP",
    "Windows 2008": "VISTA",
    "Linux": "LINUX"
}

class SaunterTestCase(BaseTestCase):
    def setUp(self):
        self.verificationErrors = []
        self.cf = saunter.ConfigWrapper.ConfigWrapper().config
        if self.cf.getboolean("SauceLabs", "ondemand"):
            desired_capabilities = {
                "platform": self.cf.get("SauceLabs", "os"),
                "browserName": self.cf.get("SauceLabs", "browser"),
                "version": self.cf.get("SauceLabs", "browser_version"),
                "name": self._testMethodName
            }
            if desired_capabilities["browserName"][0] == "*":
                desired_capabilities["browserName"] = desired_capabilities["browserName"][1:]
            if desired_capabilities["platform"] in os_map:
                desired_capabilities["platform"] = os_map[desired_capabilities["platform"]]
            command_executor = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (self.cf.get("SauceLabs", "username"), self.cf.get("SauceLabs", "key"))
        else:
            browser = self.cf.get("Selenium", "browser")
            if browser[0] == "*":
                browser = browser[1:]
            if browser in desired_capabilities:
                desired_capabilities = desired_capabilities[browser]
            command_executor = "http://%s:%s/wd/hub" % (self.cf.get("Selenium", "server_host"), self.cf.get("Selenium", "server_port"))
        self.driver = wrapper().remote_webdriver(desired_capabilities = desired_capabilities, command_executor = command_executor)
        
        if self.cf.getboolean("SauceLabs", "ondemand"):
            wrapper().sauce_session = self.driver.session_id
            
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)