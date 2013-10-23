import pytest
import transaction

from pyramid import testing


@pytest.mark.usefixtures("dbtables")
class BaseTest(object):
    def setup_method(self, method):
        self._patchers = []
        self.config = testing.setUp()

    def add_patcher(self, patcher):
        self._patchers.append(patcher)
        patcher.start()
        return patcher

    def teardown_method(self, method):
        transaction.abort()
        testing.tearDown()
        for patcher in self._patchers:
            patcher.stop()


