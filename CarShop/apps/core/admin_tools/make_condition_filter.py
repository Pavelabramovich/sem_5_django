from apps.core.db_tools import queryset_condition_filter
from django.contrib import admin


def make_condition_filter(condition, title_, parameter_name_):
    class ConditionListFilter(admin.SimpleListFilter):
        title = title_
        parameter_name = parameter_name_

        def lookups(self, request, model_admin):
            return [
                ("yes", "Yes"),
                ("no", "No"),
            ]

        def queryset(self, request, queryset):
            if self.value() == "yes":
                return queryset_condition_filter(queryset, condition)

            elif self.value() == "no":
                negative_condition = lambda obj: not condition(obj)
                return queryset_condition_filter(queryset, negative_condition)

    return ConditionListFilter
