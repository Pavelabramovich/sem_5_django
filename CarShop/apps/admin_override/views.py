from django.contrib import admin
from datetime import datetime
from dateutil.relativedelta import relativedelta
from math import ceil
from django.contrib.admin.apps import AdminConfig
import json
from collections import Counter

from apps.core.basic_tools import internet_connection_exists


class CustomViewsAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        from apps.shop.models import Category
        from django.contrib.auth.models import User

        categories = Category.objects.all()
        categories_counts = []

        for index, category in enumerate(categories):
            category_count = len(category.product_set.all())
            categories_counts.append([category.name, category_count])

        users = User.objects.all()
        date_list = []

        def months_diff(start, end):
            return ceil((end - start).days / 30)

        month_kwargs = dict(day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

        today_month = datetime.today().replace(**month_kwargs)
        min_month = datetime.max.replace(**month_kwargs)

        for user in users:
            user_dj_month = user.date_joined.replace(**month_kwargs)

            if user_dj_month < min_month:
                min_month = user_dj_month

            date_list.append(user_dj_month)

        date_counts = Counter(date_list)

        all_months = []
        month_delta = relativedelta(months=+1)

        while min_month <= today_month:
            all_months.append(min_month)
            min_month += month_delta

        tmp_sum = 0

        users_per_months = []

        for month in all_months:
            if count := date_counts.get(month):
                tmp_sum += count

            if months_diff(month, today_month) < 12:
                users_per_months.append([month.isoformat(), tmp_sum])

        return super().index(request, extra_context={'categories_counts': json.dumps(categories_counts),
                                                     'users_per_months': json.dumps(users_per_months),
                                                     'internet_connection_exists': internet_connection_exists()})
