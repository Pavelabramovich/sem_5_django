from importlib.util import find_spec
import unittest

from django.apps import apps
from django.conf import settings
from django.test.runner import DiscoverRunner
from django.db import models


class TestLoader(unittest.TestLoader):
    def __init__(self, *args, runner, **kwargs):
        self.runner = runner
        super().__init__(*args, **kwargs)

    def loadTestsFromModule(self, module, *args, pattern=None, **kws):
        suite = super().loadTestsFromModule(module, pattern)
        if suite.countTestCases():
            self.runner.register_test_module(module)

        return suite


class RunnerWithTestModels(DiscoverRunner):
    # Test Runner that will add any test packages with a 'models' module to INSTALLED_APPS.
    # Allows test only models to be defined within any package that contains tests.
    # All test models should be set with app_label = 'tests'

    def __init__(self, *args, **kwargs):
        self.test_packages = set()
        self.test_loader = TestLoader(runner=self)
        super().__init__(*args, **kwargs)

    def register_test_module(self, module):
        self.test_packages.add(module.__package__)

    def setup_databases(self, **kwargs):
        test_apps = {package for package in self.test_packages if find_spec('.models', package)}

        new_installed = list(settings.INSTALLED_APPS) + list(set(test_apps).difference(settings.INSTALLED_APPS))
        apps.set_installed_apps(new_installed)

        return super().setup_databases(**kwargs)


class TestModel(models.Model):
    class Meta:
        app_label = 'tests'
        abstract = True
