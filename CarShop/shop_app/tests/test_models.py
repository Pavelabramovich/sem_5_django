import datetime

from django.test import TestCase
from test_app.models import Category, Provider, Producer, Buy, Product


class TestCategoryModel(TestCase):
    def setUp(self):
        self.test_obj = Category.objects.create(name='Tire')

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
        expected_absolute_url = f'/category/Tire/'
        self.assertEqual(category.get_absolute_url(), expected_absolute_url)


class TestProviderModel(TestCase):
    def setUp(self):
        self.test_obj = Provider.objects.create(name='Richard',
                                                phone='+375 (29) 123-45-67',
                                                address="Red alley 1, Bricklin")

    def test_str(self):
        provider = self.test_obj
        expected_str_res = 'Richard'
        self.assertEqual(str(provider), expected_str_res)

    def test_get_absolute_url(self):
        provider = self.test_obj
        expected_absolute_url = f'/provider/Richard/'
        self.assertEqual(provider.get_absolute_url(), expected_absolute_url)


class TestProducerModel(TestCase):
    def setUp(self):
        self.test_obj = Producer.objects.create(name='Peter',
                                                phone='+375 (29) 987-65-43',
                                                address="Grand highway 1, Lowfield")

    def test_str(self):
        producer = self.test_obj
        expected_str_res = 'Peter'
        self.assertEqual(str(producer), expected_str_res)

    def test_get_absolute_url(self):
        provider = self.test_obj
        expected_absolute_url = f'/producer/Peter/'
        self.assertEqual(provider.get_absolute_url(), expected_absolute_url)


class TestBuyModel(TestCase):
    def setUp(self):
        date = datetime.date(2023, 7, 20)
        product_name = "Cheap wheel"
        count = 4

        self.test_obj = Buy.objects.create(date=date, product_name=product_name, count=count)

    def test_str(self):
        buy = self.test_obj
        expected_str_res = 'Buy Cheap wheel x4'
        self.assertEqual(str(buy), expected_str_res)

    def test_get_absolute_url(self):
        pass
        # provider = self.test_obj
        # expected_absolute_url = f'/b/Peter/'
        # self.assertEqual(provider.get_absolute_url(), expected_absolute_url)


class TestProductModel(TestCase):
    def setUp(self):
        name = 'Expensive wipers'
        category = Category.objects.create(name='Cleaners')
        price = 100

        producer = Producer.objects.create(name='Valentin',
                                           phone='+375 (29) 375-95-21',
                                           address="Tiny street 14, High Hills")

        providers = [
            Provider.objects.create(name='Vova',
                                    phone='+375 (29) 501-20-09',
                                    address="Smoky Lane 58, Smoglin"),
            Provider.objects.create(name='Vasya',
                                    phone='+375 (29) 039-28-11',
                                    address="Low avenue 37, Tromburg"),
            Provider.objects.create(name='Vlad',
                                    phone='+375 (29) 984-02-53',
                                    address="Quiet allay 8, Monday"),
        ]

        self.test_obj = Product.objects.create(name=name,
                                               category=category,
                                               price=price,
                                               producer=producer)
        for i in range(1, 4):
            self.test_obj.providers.add(i)

    def test_str(self):
        product = self.test_obj
        expected_str_res = 'Expensive wipers'
        self.assertEqual(str(product), expected_str_res)

    def test_get_absolute_url(self):
        pass
        # provider = self.test_obj
        # expected_absolute_url = f'/producer/Peter/'
        #  self.assertEqual(provider.get_absolute_url(), expected_absolute_url)
