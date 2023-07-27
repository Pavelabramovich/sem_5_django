from django.test import TestCase
from test_app.models import Category


class TestCategoryModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_obj = Category.objects.create(name='Tire')

    def test_name_label(self):
        category = self.test_obj
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        category = self.test_obj
        max_length = category._meta.get_field('name').max_length
        self.assertEqual(max_length, 64)

    def test_str(self):
        category = self.test_obj
        expected_str_res = 'Tire'
        self.assertEqual(str(category), expected_str_res)

    def test_get_absolute_url(self):
        category = self.test_obj
        expected_absolute_url = f'/category/{category.name}/'
        self.assertEqual(category.get_absolute_url(), expected_absolute_url)
