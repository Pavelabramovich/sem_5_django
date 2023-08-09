def filter_primary_keys(queryset, condition):
    return [obj.pk for obj in queryset if condition(obj)]


def queryset_condition_filter(queryset, condition):
    filtered_primary_keys = filter_primary_keys(queryset, condition)
    return queryset.filter(pk__in=filtered_primary_keys)
