from django.contrib.admin import FieldListFilter


def make_range_field_list_filter(lookups, nullable=False):
    class RangeFieldListFilter(FieldListFilter):
        def __init__(self, field, request, params, model, model_admin, field_path):
            self.field_generic = '%s__' % field_path
            self.range_params = dict([(k, v) for k, v in params.items()
                                     if k.startswith(self.field_generic)])

            self.lookup_kwarg_start = '%s__gte' % field_path
            self.lookup_kwarg_stop = '%s__lt' % field_path
            self.lookup_kwarg_null = '%s__isnull' % field_path

            self.links = [('All', {}), ]
            for name, start, stop in lookups:
                query_params = {}
                if start is not None:
                    query_params[self.lookup_kwarg_start] = str(start)
                if stop is not None:
                    query_params[self.lookup_kwarg_stop] = str(stop)

                self.links.append((name, query_params))

            if nullable:
                self.links.append(('Unknown', {
                    self.lookup_kwarg_null: 'True'
                }))

            super(RangeFieldListFilter, self).__init__(
                field, request, params, model, model_admin, field_path)

        def expected_parameters(self):
            return [
                self.lookup_kwarg_start,
                self.lookup_kwarg_stop,
                self.lookup_kwarg_null
            ]

        def choices(self, cl):
            for title, param_dict in self.links:
                yield {
                    'selected': self.range_params == param_dict,
                    'query_string': cl.get_query_string(
                                        param_dict, [self.field_generic]),
                    'display': title,
                }

    return RangeFieldListFilter
