import traceback
from unittest.case import _AssertRaisesContext


class _AssertNotRaisesContext(_AssertRaisesContext):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            self.exception = exc_value.with_traceback(None)

            if not issubclass(exc_type, self.expected):
                return False

            exc_name = self.expected.__name__

            if self.obj_name:
                self._raiseFailure(f"{exc_name} unexpectedly raised by {self.obj_name}")
            else:
                self._raiseFailure(f"{exc_name} unexpectedly raised")

        else:
            traceback.clear_frames(tb)

        return True


class AssertNotRaisesMixin:
    def assertNotRaises(self, expected_exception, *args, **kwargs):
        context = _AssertNotRaisesContext(expected_exception, self)
        try:
            return context.handle('assertNotRaises', args, kwargs)
        finally:
            context = None
