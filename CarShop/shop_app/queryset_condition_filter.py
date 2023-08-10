def queryset_condition_filter(queryset, condition):
    filtered_primary_keys = [obj.pk for obj in queryset if condition(obj)]
    return queryset.filter(pk__in=filtered_primary_keys)
