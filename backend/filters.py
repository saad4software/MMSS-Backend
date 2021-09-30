from django_filters import rest_framework as filters
from .models import *


class MotivationDateFilter(filters.FilterSet):
    min_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    max_date = filters.DateFilter(field_name="date", lookup_expr="lte")
    is_active = filters.BooleanFilter(field_name="isActive")

    emp_id = filters.NumberFilter(field_name="employee__id")


class Meta:
        model = Motivation
        fields = ['min_date', 'max_date', 'is_active', 'emp_id', ]


class PaymentDateFilter(filters.FilterSet):
    min_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    max_date = filters.DateFilter(field_name="date", lookup_expr="lte")
    sub_id = filters.NumberFilter(field_name="subscription__id")
    is_active = filters.BooleanFilter(field_name="isActive")

    class Meta:
        model = Payment
        fields = ['min_date', 'max_date', 'is_active', 'sub_id']


class TransactionDateFilter(filters.FilterSet):
    min_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    max_date = filters.DateFilter(field_name="date", lookup_expr="lte")
    is_active = filters.BooleanFilter(field_name="isActive")

    class Meta:
        model = Transaction
        fields = ['min_date', 'max_date', 'is_active']


class EmployeeDataFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name="isActive")

    class Meta:
        model = Employee
        fields = ['is_active']


class ProjectDataFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name="isActive")

    class Meta:
        model = Project
        fields = ['is_active']


class RatioDataFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name="isActive")

    class Meta:
        model = Ratio
        fields = ['is_active']


class ClientDataFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name="isActive")

    class Meta:
        model = Client
        fields = ['is_active']


class SpaceDataFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name="isActive")

    class Meta:
        model = Space
        fields = ['is_active']


class SubscriptionDateFilter(filters.FilterSet):
    min_date_from = filters.DateFilter(field_name="from_date", lookup_expr="gte")
    max_date_from = filters.DateFilter(field_name="from_date", lookup_expr="lte")

    min_date_to = filters.DateFilter(field_name="to_date", lookup_expr="gte")
    max_date_to = filters.DateFilter(field_name="to_date", lookup_expr="lte")

    is_active = filters.BooleanFilter(field_name="isActive")

    client_id = filters.NumberFilter(field_name="client__id")
    project_id = filters.NumberFilter(field_name="project__id")

    class Meta:
        model = Subscription
        fields = ['min_date_from', 'max_date_from', 'min_date_to', 'max_date_to', 'is_active', 'client_id', 'project_id', ]

