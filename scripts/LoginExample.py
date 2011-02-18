import CustomTestCase

from pages.HomePage import HomePage

from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest

class LoginExample(CustomTestCase.CustomTestCase):
    @attr(tags=['deep', 'website', 'login'])
    def incorrect_login(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        l.username = "foo"
        l.password = "bar"
        l.do_login()
        self.assertEqual(l.error_message, "Incorrect username or password.")

    @attr(tags=['deep', 'website', 'login'])
    def incorrect_login_with_soft_assert(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        l.username = "foo"
        l.password = "bar"
        l.do_login()
        self.verifyEqual(l.error_message, "Incorrect username or password.")