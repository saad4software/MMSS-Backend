from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import FileField, ListField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from django.db.models import Sum


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']

        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'password1', 'password2',
            'first_name', 'last_name',
            'role',
        )
        read_only_fields = ('id',)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra fields
        data['role'] = self.user.role
        return data


# not used
class LogInSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'id', 'isActive']
        ordering = ['name']


class SpacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ['name', 'id']
        ordering = ['name']


class EmployeeSerializer(serializers.ModelSerializer):

    # motivations = serializers.PrimaryKeyRelatedField(many=True, queryset=Motivation.objects.all())

    class Meta:
        model = Employee
        fields = ['name', 'id', 'gender', 'hiring_date',
                  'leaving_date', 'phone', 'address',
                  'image', 'notes', 'fixed_salary', 'isActive' ]
        ordering = ['name']


class MotivationsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = Motivation
        fields = ['amount', 'type', 'date', 'notes',
                  'employee', 'id', 'name', 'isActive']
        ordering = ['employee.name']
        # depth = 1


class RatioSerializer(serializers.ModelSerializer):
    projectName = serializers.CharField(source='project.name', read_only=True)
    employeeName = serializers.CharField(source='employee.name', read_only=True)
    spaceName = serializers.CharField(source='space.name', read_only=True)

    class Meta:
        model = Ratio
        fields = ['employee', 'project', 'ratio', 'thresh', 'id',
                  'notes', 'projectName', 'isActive', 'projectName',
                  'employeeName', 'space', 'spaceName', ]
        ordering = ['employee.name']
        # depth = 1


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'ceo_name', 'phone', 'fax', 'id',
                  'mobile', 'address', 'work_field', 'notes', ]
        ordering = ['name']


class SubscriptionSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    employees_list = EmployeeSerializer(source='employees', read_only=True, many=True)
    employee_owner = EmployeeSerializer(source='owner', read_only=True)
    spaces_list = SpacesSerializer(source='spaces', read_only=True, many=True)

    payments_sum = serializers.FloatField(read_only=True, default=0)
    ratio = serializers.FloatField(read_only=True, default=0)
    thresh = serializers.FloatField(read_only=True, default=0)
    pay = serializers.FloatField(read_only=True, default=0)

    class Meta:
        model = Subscription
        fields = ['from_date', 'to_date', 'amount', 'paper_id',
                  'notes', 'isActive', 'project', 'client', 'employees',
                  'spaces', 'project_name', 'client_name', 'id', 'payments_sum',
                  'ratio', 'thresh', 'owner', 'pay', 'employees_list',
                  'spaces_list', 'employee_owner']

        ordering = ['client_name']


class PaymentSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='subscription.client.name', read_only=True)
    subscription_id = serializers.CharField(source='subscription.paper_id', read_only=True)
    # subscription = SubscriptionSerializer(read_only=True, many=False)

    class Meta:
        model = Payment
        fields = ['amount', 'paper_id', 'date', 'notes', 'subscription',
                  'id', 'client_name', 'isActive', 'subscription_id', ]
        ordering = ['date']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'type', 'date', 'notes', 'isActive', 'id' ]
        ordering = ['date']



