def first_or_default(col, condition=lambda obj: True, default=None):
    return next((obj for obj in col if condition(obj)), default)
