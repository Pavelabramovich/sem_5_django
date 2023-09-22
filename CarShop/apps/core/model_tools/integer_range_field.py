from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class IntegerRangeField(models.IntegerField):
    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value

        validate_min_value = MinValueValidator(min_value)
        validate_max_value = MaxValueValidator(max_value)

        if 'validators' in kwargs:
            validators = kwargs['validators']
        else:
            validators = []

        if min_value is not None and validate_min_value not in validators:
            validators.append(MinValueValidator(min_value))

        if max_value is not None and validate_max_value not in validators:
            validators.append(MaxValueValidator(max_value))

        kwargs['validators'] = validators

        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["min_value"] = self.min_value
        kwargs["max_value"] = self.max_value
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        kwargs.update({'min_value': self.min_value, 'max_value': self.max_value})
        return super(IntegerRangeField, self).formfield(**kwargs)
