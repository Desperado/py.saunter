"""
========
BasePage
========
"""
from pages import timeout_seconds
from CustomException import ElementVisiblityTimeout, ElementTextTimeout
import time

class BasePage(object):
    """
    Top of the PO page tree
    """
    def is_element_available(self, locator):
        """
        Synchronization method for making sure the element we're looking for is not only on the page,
        but also visible -- since Se will happily deal with things that aren't visible.
        
        Use this instead of is_element_present most of the time.
        """
        if self.se.is_element_present(locator):
            if self.se.is_visible(locator):
                return True
            else:
                return False
        else:
            return False
            
    def wait_for_visible(self, locator):
        """
        Synchronization to deal with elements that are present, but are disabled until some action
        triggers their visibility.
        
        :raises: ElementVisiblityTimeout        
        """
        for i in range(timeout_seconds):
            try:
                if self.se.is_visible(locator):
                    break
            except:
                pass
            time.sleep(1)
        else:
            raise ElementVisiblityTimeout("%s visibility timed out" % locator)
        return True

    def wait_for_hidden(self, locator):
        """
        Synchronization to deal with elements that are present, but are visibility until some action
        triggers their hidden-ness.

        :raises: ElementVisiblityTimeout=
        """
        for i in range(timeout_seconds):
            if self.se.is_visible(locator):
                time.sleep(1)
            else:
                break
        else:
            raise ElementVisiblityTimeout("%s visibility timed out" % locator)
        return True
            
    def wait_for_text(self, locator, text):
        """
        Synchronization on some text being displayed in a particular element.

        :raises: ElementVisiblityTimeout
        """
        for i in range(timeout_seconds):
            try:
                if self.se.get_text(locator) == text:
                    break
            except:
                pass
            time.sleep(1)
        else:
            raise ElementTextTimeout("%s value timed out" % locator)
        return True

    def wait_for_value(self, locator, text):
        """
        Synchronization on some value being set in a particular element.

        :raises: ElementVisiblityTimeout

        """
        for i in range(timeout_seconds):
            try:
                if self.se.get_value(locator) == text:
                    break
            except:
                pass
            time.sleep(1)
        else:
            raise ElementTextTimeout("%s value timed out" % locator)
        return True
            
    def wait_for_element_not_present(self, locator):
        """
        Synchronization helper to wait until some element is removed from the page 

        :raises: ElementVisiblityTimeout
        """
        for i in range(timeout_seconds):
            if self.se.is_element_present(locator):
                time.sleep(1)
            else:
                break
        else:
            raise ElementVisiblityTimeout("%s presence timed out" % locator)
        return True