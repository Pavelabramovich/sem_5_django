class ViewOnlyFieldsAdminMixin:
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)

        if hasattr(self, 'only_view_fields') and db_field.name in self.only_view_fields:
            formfield.widget.can_add_related = False
            formfield.widget.can_change_related = False
            formfield.widget.can_delete_related = False

        return formfield
