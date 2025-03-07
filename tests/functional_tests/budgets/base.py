import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from budgets.tests.test_budget_base import BudgetMixin
from utils.browser import make_chrome_browser


class BudgetBaseFunctionalTest(StaticLiveServerTestCase, BudgetMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)