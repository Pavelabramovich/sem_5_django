class FieldsWidgetsMixin:
    def formfield_for_dbfield(self, db_field, **kwargs):
        if widget := getattr(self, 'fields_widgets', {}).get(db_field.name):
            kwargs['widget'] = widget

        return super().formfield_for_dbfield(db_field, **kwargs)
