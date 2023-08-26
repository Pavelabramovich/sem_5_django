from django.test import TestCase

from apps.core.test_tools import AssertNotRaisesMixin


class TestAssertNotRaisesMixin(TestCase):
    def setUp(self):
        self.test_case_class = type("CustomTestCase", (AssertNotRaisesMixin, TestCase), {})
        self.test_case = self.test_case_class()

        self.first_exception_type = type("FirstException", (Exception,), {})
        self.second_exception_type = type("SecondException", (Exception,), {})

    @staticmethod
    def raise_exception(exception_type, *args, **kwargs):
        if exception_type:
            raise exception_type(*args, **kwargs)

    def test_context_manager_expected_raised(self):
        test_case = self.test_case
        test_case_class = self.test_case_class

        first_exception_type = self.first_exception_type

        with self.assertRaises(test_case_class.failureException):
            with test_case.assertNotRaises(first_exception_type):
                self.raise_exception(first_exception_type)

    def test_context_manager_unexpected_raised(self):
        test_case = self.test_case

        first_exception_type = self.first_exception_type
        second_exception_type = self.second_exception_type

        with self.assertRaises(second_exception_type):
            with test_case.assertNotRaises(first_exception_type):
                self.raise_exception(second_exception_type)

    def test_context_manager_not_raised(self):
        test_case = self.test_case
        test_case_class = self.test_case_class

        first_exception_type = self.first_exception_type

        try:
            with test_case.assertNotRaises(first_exception_type):
                self.raise_exception(None)
        except test_case_class.failureException as error:
            self.fail(f"{type(error).__name__} unexpectedly raised")

    def test_function_expected_raised(self):
        test_case = self.test_case
        test_case_class = self.test_case_class

        first_exception_type = self.first_exception_type

        with self.assertRaises(test_case_class.failureException):
            test_case.assertNotRaises(first_exception_type, self.raise_exception, first_exception_type)

    def test_function_unexpected_raised(self):
        test_case = self.test_case

        first_exception_type = self.first_exception_type
        second_exception_type = self.second_exception_type

        with self.assertRaises(second_exception_type):
            test_case.assertNotRaises(first_exception_type, self.raise_exception, second_exception_type)

    def test_function_not_raised(self):
        test_case = self.test_case
        test_case_class = self.test_case_class

        first_exception_type = self.first_exception_type

        try:
            test_case.assertNotRaises(first_exception_type, self.raise_exception, None)
        except test_case_class.failureException as error:
            self.fail(f"{type(error).__name__} unexpectedly raised")
