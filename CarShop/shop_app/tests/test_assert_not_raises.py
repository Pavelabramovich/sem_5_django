from django.test import TestCase
from unittest import case
from django.forms import ValidationError
from shop_app.tests.assert_not_raises_mixin import _AssertNotRaisesContext


class TestAssertNotRaisesContext(TestCase):
    def setUp(self):
        test_case = case.TestCase()
        self.test_context = _AssertNotRaisesContext(ValidationError, test_case)

    def test_not_raised(self):
        test_context = self.test_context
        res = test_context.__exit__(None, None, None)
        self.assertTrue(res)

    def test_expected_raised(self):
        with self.assertRaises(TestCase.failureException):
            test_context = self.test_context
            exception = ValidationError("Message")
            res = test_context.__exit__(type(exception), exception, exception.__traceback__)

    def test_unexpected_raised(self):
        test_context = self.test_context
        exception = ValueError("Message")
        res = test_context.__exit__(type(exception), exception, exception.__traceback__)
        self.assertFalse(res)


