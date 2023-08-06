from django import forms


class FieldsetsInlineMixin:
    change_form_template = 'admin/admin_inlines_to_fieldsets_change_form.html'

    def get_fieldsets(self, request, obj=None):
        if hasattr(self, 'fieldsets_with_inlines'):
            return self._replace_inlines_with_placeholders(self.fieldsets_with_inlines)
        else:
            return super().get_fieldsets(request, obj)

    def get_inline_instances(self, request, obj=None):
        if hasattr(self, 'fieldsets_with_inlines'):
            inlines = self._filter_inlines(self.fieldsets_with_inlines)
            return self._get_inline_instances_from_inlines(request, inlines, obj)
        else:
            return super().get_inline_instances(request, obj)

    @staticmethod
    def _replace_inlines_with_placeholders(fieldsets):
        res = []

        for index, fieldset in enumerate(fieldsets):
            if isinstance(fieldset, forms.MediaDefiningClass):
                fieldset.fieldset_index = index
                res.append((None, {'fields': ()}))
            else:
                res.append(fieldset)

        return res

    @staticmethod
    def _filter_inlines(fieldsets):
        return [fieldset for fieldset in fieldsets if isinstance(fieldset, forms.MediaDefiningClass)]

    def _get_inline_instances_from_inlines(self, request, inlines, obj):
        inline_instances = []

        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_add_permission(request, obj) or
                        inline.has_change_permission(request, obj) or
                        inline.has_delete_permission(request, obj)):
                    continue
                if not inline.has_add_permission(request, obj):
                    inline.max_num = 0
            inline_instances.append(inline)

        return inline_instances


class UserFieldsetsInlineMixin(FieldsetsInlineMixin):
    add_form_template = 'admin/admin_inlines_to_fieldsets_add_form.html'

    def get_fieldsets(self, request, obj=None):
        if not obj:
            if hasattr(self, 'add_fieldsets_with_inlines'):
                return self._replace_inlines_with_placeholders(self.add_fieldsets_with_inlines)
            else:
                return super(FieldsetsInlineMixin, self).get_fieldsets(request, obj)
        else:
            return super().get_fieldsets(request, obj)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            if hasattr(self, 'add_fieldsets_with_inlines'):
                inlines = self._filter_inlines(self.add_fieldsets_with_inlines)
                return self._get_inline_instances_from_inlines(request, inlines, obj)
            else:
                return super(FieldsetsInlineMixin, self).get_inline_instances(request, obj)
        else:
            return super().get_inline_instances(request, obj)
