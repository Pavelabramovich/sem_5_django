from django import forms


class FieldsetsInlineMixin:
    change_form_template = 'admin/admin_inlines_to_fieldsets_change_form.html'

    @staticmethod
    def make_placeholder(index, fieldset):
        if isinstance(fieldset, forms.MediaDefiningClass):
            fieldset.fieldset_index = index
            return None, {'fields': ()}
        else:
            return fieldset

    def get_fieldsets(self, request, obj=None):
        if self.fieldsets_with_inlines:
            return [
                self.make_placeholder(index, fieldset)
                for index, fieldset in enumerate(self.fieldsets_with_inlines)]
        else:
            return super().get_fieldsets(request, obj)

    def get_inline_instances(self, request, obj=None):
        if self.fieldsets_with_inlines:
            inlines = [
                inline for inline in self.fieldsets_with_inlines
                if isinstance(inline, forms.MediaDefiningClass)]
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

        else:
            return super().get_inline_instances(request, obj)
