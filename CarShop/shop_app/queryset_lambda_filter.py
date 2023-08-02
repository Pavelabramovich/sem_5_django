def queryset_lambda_filter(queryset, func_filter):
    filtered_primary_keys = [obj.pk for obj in queryset if func_filter(obj)]
    return queryset.filter(pk__in=filtered_primary_keys)
