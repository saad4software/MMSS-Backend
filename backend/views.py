import django_filters.rest_framework
import rest_framework.filters
from django.shortcuts import render

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from .serializers import *
from .models import *
from rest_framework import generics, status
from django_filters import rest_framework as filters
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .permissions import IsCounter, IsGuest, IsAdmin
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .filters import *
from django.db.models import *
from django.utils.dateparse import parse_date
from rest_pandas import PandasView, PandasSimpleView, PandasMixin


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "status": "success",
            "code": status_code,
            "data": data,
            "message": None
        }
        if not str(status_code).startswith('2'):
            response["status"] = "error"
            response["data"] = None

            if 'detail' in data:
                response["message"] = data["detail"]
            else:
                response['message'] = dict2string(data)

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


def dict2string(data):
    msg = ""
    for key in data.keys():
        msg += key + ": " + data[key][0] + "\n\r"
    return msg


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        username = request.user
        user = User.objects.get(id=request.user.id)
        userid = request.user.id
        content = {'message': request.user.role}
        return Response(content)


class TokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class UsersCreate(generics.CreateAPIView):
    permission_classes = (IsAdmin,)

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class UsersList(generics.ListAPIView):
    permission_classes = (IsAdmin,)

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [rest_framework.filters.SearchFilter]
    search_fields = ['username']
    pagination_class = StandardResultsSetPagination


class UsersUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    lookup_field = 'id'


class ProjectsList(generics.ListAPIView):
    permission_classes = (IsGuest, )

    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    filterset_class = ProjectDataFilter
    search_fields = ['name']
    pagination_class = StandardResultsSetPagination


class ProjectsCreate(generics.CreateAPIView):
    permission_classes = (IsCounter, )

    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class ProjectsUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsCounter, )

    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    lookup_field = 'id'


class SpacesList(generics.ListAPIView):
    permission_classes = (IsGuest, )

    queryset = Space.objects.all()
    serializer_class = SpacesSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    filterset_class = SpaceDataFilter
    search_fields = ['name']
    pagination_class = StandardResultsSetPagination


class SpacesCreate(generics.CreateAPIView):
    permission_classes = (IsCounter, )

    queryset = Space.objects.all()
    serializer_class = SpacesSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class SpacesUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsCounter, )

    queryset = Space.objects.all()
    serializer_class = SpacesSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class EmployeesList(generics.ListAPIView):
    permission_classes = (IsGuest, )

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    filterset_class = EmployeeDataFilter
    search_fields = ['name', 'notes']
    pagination_class = StandardResultsSetPagination

# filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['name']
    # filter_backends = [rest_framework.filters.SearchFilter]
    # search_fields = ['name']


class EmployeesCreate(generics.CreateAPIView):
    permission_classes = (IsCounter, )

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class EmployeesUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsCounter, )
    lookup_field = 'id'

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class MotivationsList(generics.ListAPIView):
    permission_classes = (IsAdmin, )

    queryset = Motivation.objects.all()
    serializer_class = MotivationsSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter, rest_framework.filters.OrderingFilter]
    search_fields = ['employee__name']
    ordering_fields = ('type', 'date', 'employee__name')
    filterset_class = MotivationDateFilter
    pagination_class = StandardResultsSetPagination


class MotivationsCreate(generics.CreateAPIView):
    permission_classes = (IsAdmin, )

    queryset = Motivation.objects.all()
    serializer_class = MotivationsSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def perform_create(self, serializer):
        serializer.save()
        if serializer.data['type'] == 'L' and serializer.data['amount'] > 0:
            emp = Employee.objects.get(pk=serializer.data['employee'])
            transaction = Transaction(
                amount=serializer.data['amount'],
                type='O',
                date=datetime.now(),
                notes=emp.name + ' loan',
                isActive=True)
            transaction.save()


class MotivationsUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin, )
    lookup_field = 'id'

    queryset = Motivation.objects.all()
    serializer_class = MotivationsSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class RatiosList(generics.ListAPIView):
    permission_classes = (IsAdmin, )

    queryset = Ratio.objects.all()
    serializer_class = RatioSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    search_fields = ['employee__name', 'project__name']
    pagination_class = StandardResultsSetPagination
    filterset_class = RatioDataFilter


class RatiosCreate(generics.CreateAPIView):
    permission_classes = (IsAdmin, )

    queryset = Ratio.objects.all()
    serializer_class = RatioSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class RatiosUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin, )
    lookup_field = 'id'

    queryset = Ratio.objects.all()
    serializer_class = RatioSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class ClientsList(generics.ListAPIView):
    permission_classes = (IsGuest, )

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    search_fields = ['name', 'ceo_name', 'phone', 'mobile', 'fax', ]
    pagination_class = StandardResultsSetPagination
    filterset_class = ClientDataFilter


class ClientsCreate(generics.CreateAPIView):
    permission_classes = (IsCounter, )

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class ClientUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsCounter, )
    lookup_field = 'id'

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class SubscriptionsList(generics.ListAPIView):
    permission_classes = (IsCounter, )

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    search_fields = ['paper_id', 'notes', 'project__name', 'client__name','owner__name' ]
    pagination_class = StandardResultsSetPagination
    filterset_class = SubscriptionDateFilter


class SubscriptionCreate(generics.CreateAPIView):
    permission_classes = (IsCounter, )

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class SubscriptionUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsCounter, )
    lookup_field = 'id'

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class PaymentList(generics.ListAPIView):
    permission_classes = (IsCounter, )

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    search_fields = ['paper_id', 'notes', 'subscription__client__name']
    pagination_class = StandardResultsSetPagination
    filterset_class = PaymentDateFilter


class PaymentCreate(generics.CreateAPIView):
    permission_classes = (IsCounter, )

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def perform_create(self, serializer):
        serializer.save
        sub = Subscription.objects.get(pk=serializer.data['subscription'])
        transaction = Transaction(
            amount=serializer.data['amount'],
            type='I',
            date=datetime.now(),
            notes=sub.client.name + ' subscription',
            isActive=True)
        transaction.save()


class PaymentUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsCounter, )
    lookup_field = 'id'

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class TransactionList(generics.ListAPIView):
    permission_classes = (IsCounter, )

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.DjangoFilterBackend, rest_framework.filters.SearchFilter]
    search_fields = ['notes']
    pagination_class = StandardResultsSetPagination
    filterset_class = TransactionDateFilter


class TransactionCreate(generics.CreateAPIView):
    permission_classes = (IsCounter, )

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class TransactionUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsCounter, )
    lookup_field = 'id'

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]




class TimeSeriesView(PandasView):
    permission_classes = ()
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    # That's it!  The view will be able to export the model dataset to any of
    # the included formats listed above.  No further customization is needed to
    # leverage the defaults.


class SalaryReport(APIView):
    permission_classes = ( )
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request):
        employee_id = int(request.GET['id'])
        date = parse_date(request.GET['date'])
        print(date)
        month = date.month
        year = date.year

        employee = Employee.objects.all().get(id=employee_id)
        base_salary = 0 if employee.fixed_salary is None else employee.fixed_salary

        name = employee.name
        rewards = Motivation.objects.filter(
            isActive=True,
            date__month=month,
            date__year=year,
            employee__id=employee_id,
            type='R'
        ).values('amount', 'date', 'notes')
        rewards_sum = rewards.aggregate(Sum('amount'))['amount__sum']
        rewards_sum = 0 if rewards_sum is None else rewards_sum

        cut_offs = Motivation.objects.filter(
            isActive=True,
            date__month=month,
            date__year=year,
            employee__id=employee_id,
            type='C'
        ).values('amount', 'date', 'notes')
        cut_offs_sum = cut_offs.aggregate(Sum('amount'))['amount__sum']
        cut_offs_sum = 0 if cut_offs_sum is None else cut_offs_sum

        loans = Motivation.objects.filter(
            isActive=True,
            date__month=month,
            date__year=year,
            employee__id=employee_id,
            type='L',
            amount__lte=0,
        ).values('amount', 'date', 'notes')
        loans_sum = loans.aggregate(Sum('amount'))['amount__sum']
        loans_sum = 0 if loans_sum is None else loans_sum

        subscriptions = Subscription.objects.filter(employees__id=employee_id, isActive=True)\
            .annotate(payments_sum=Sum('payments__amount'))\
            .annotate(payment_date=Max('payments__date'))\
            .filter(payment_date__month=month, payment_date__year=year)\
            .annotate(ratio=Subquery(Ratio.objects.filter(project__id=OuterRef('project__id'), employee__id=employee_id).values('ratio')))\
            .annotate(thresh=Subquery(Ratio.objects.filter(project__id=OuterRef('project__id'), space__id=OuterRef('spaces__id'), employee__id=employee_id).values('thresh')))\
            .annotate(pay=Case(
                When(
                    payments_sum__lt=F('amount'),
                    then=0.0
                    ),

                When(
                    amount__gt=F('thresh'),
                    then=F('amount')-F('thresh')+F('thresh')*F('ratio')/100
                    ),

                default=F('amount')*F('ratio')/100
                )
            ).values('pay', 'thresh', 'amount', 'ratio', 'client__name', 'project__name')
        subscriptions_sum = subscriptions.aggregate(Sum('pay'))['pay__sum']
        subscriptions_sum = 0 if subscriptions_sum is None else subscriptions_sum

        total = base_salary + rewards_sum - cut_offs_sum + loans_sum + subscriptions_sum

        content = {
            'name': name,
            'salary': base_salary,
            'rewards_sum': rewards_sum,
            'rewards': rewards,
            'cut_off_sum': cut_offs_sum,
            'cut_off': cut_offs,
            'loans_sum': loans_sum,
            'loans': loans,
            'subs_sum': subscriptions_sum,
            'total': total,
            'subs': subscriptions
        }
        return Response(content)

    def post(self, request):
        content = {"res": request.data['hello']}
        return Response(content)


class SubscriptionReport(APIView):
    permission_classes = ( )
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request):
        from_data = parse_date(request.GET['from'])
        to_data = parse_date(request.GET['to'])

        subscriptions = Subscription.objects.filter(from_date__lte=to_data, from_date__gte=from_data, isActive=True)\
            .annotate(payments_sum=Sum('payments__amount'))\
            .annotate(payment_date=Max('payments__date'))\
            .annotate(pay1_amount=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[0:].values('amount')))\
            .annotate(pay1_date=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[0:].values('date')))\
            .annotate(pay2_amount=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[1:].values('amount')))\
            .annotate(pay2_date=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[1:].values('date')))\
            .annotate(pay3_amount=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[2:].values('amount')))\
            .annotate(pay3_date=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[2:].values('date')))\

        o = subscriptions.values('amount', 'client__name', 'project__name', 'from_date', 'to_date',
                                 'payments_sum', 'to_date', 'pay1_amount', 'pay1_date',
                                 'pay2_amount', 'pay2_date', 'pay3_amount', 'pay3_date')

        return Response(o)

    def post(self, request):
        content = {"res": request.data['hello']}
        return Response(content)


class NotificationsReport(APIView):
    permission_classes = ()
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request):
        # date = datetime.now()
        date = parse_date(request.GET['date']) if 'date' in request.GET else datetime.now()
        # project_id = request.GET['project_id'] if 'project_id' in request.GET else 0
        # employee_id = request.GET['employee_id'] if 'employee_id' in request.GET else 0
        # client_id = request.GET['client_id'] if 'client_id' in request.GET else 0
        #
        # print(project_id)
        # print(employee_id)
        # print(client_id)

        expired_subscriptions = Subscription.objects.filter(to_date__month=date.month, to_date__year=date.year, isActive=True)\
                .annotate(payments_sum=Sum('payments__amount'))\
                .annotate(payment_date=Max('payments__date')) \
                .annotate(renew=Subquery(Subscription.objects.filter(project__id=OuterRef('project__id'), client__id=OuterRef('client__id'), to_date__gt=OuterRef('to_date')).values('to_date'))) \
                .filter(renew__isnull=True)\
                .values('amount', 'client__name', 'project__name', 'payments_sum', 'to_date')

        due_payments = Payment.objects.filter(date__month=date.month, date__year=date.year, amount=0)\
            .values('paper_id', 'date', 'subscription__project__name', 'subscription__client__name')

        count = expired_subscriptions.count() + due_payments.count()

        content = {
            'count': count,
            'subscriptions': expired_subscriptions,
            'payments': due_payments
        }
        return Response(content)

    def post(self, request):
        content = {"res": request.data['hello']}
        return Response(content)


class ProjectsReport(APIView):
    permission_classes = (IsGuest, )
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request):
        from_data = parse_date(request.GET['from'])
        to_data = parse_date(request.GET['to'])
        project_id = request.GET['id']

        subscriptions = Subscription.objects.filter(from_date__lte=to_data, from_date__gte=from_data, project__id=project_id, isActive=True) \
            .annotate(payments_sum=Sum('payments__amount')) \
            .annotate(payment_date=Max('payments__date')) \
            .annotate(pay1_amount=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[0:].values('amount'))) \
            .annotate(pay1_date=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[0:].values('date'))) \
            .annotate(pay2_amount=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[1:].values('amount'))) \
            .annotate(pay2_date=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[1:].values('date'))) \
            .annotate(pay3_amount=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[2:].values('amount'))) \
            .annotate(pay3_date=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[2:].values('date'))) \
            .values('amount', 'client__name', 'project__name', 'from_date', 'to_date',
                    'payments_sum', 'to_date', 'pay1_amount', 'pay1_date',
                    'pay2_amount', 'pay2_date', 'pay3_amount', 'pay3_date')
        return Response(subscriptions)

    def post(self, request):
        content = {"res": request.data['hello']}
        return Response(content)


class EmployeeReport(APIView):
    permission_classes = (IsGuest, )
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request):
        from_data = parse_date(request.GET['from'])
        to_data = parse_date(request.GET['to'])
        employee_id = request.GET['id']

        subscriptions = Subscription.objects.filter(from_date__lte=to_data, from_date__gte=from_data, owner__id=employee_id, isActive=True) \
            .annotate(payments_sum=Sum('payments__amount')) \
            .annotate(payment_date=Max('payments__date')) \
            .annotate(pay1_amount=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[0:].values('amount'))) \
            .annotate(pay1_date=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[0:].values('date'))) \
            .annotate(pay2_amount=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[1:].values('amount'))) \
            .annotate(pay2_date=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[1:].values('date'))) \
            .annotate(pay3_amount=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[2:].values('amount'))) \
            .annotate(pay3_date=Subquery(Payment.objects.filter(subscription__id=OuterRef('id'))[2:].values('date'))) \
            .values('amount', 'client__name', 'project__name', 'from_date', 'to_date',
                    'payments_sum', 'to_date', 'pay1_amount', 'pay1_date',
                    'pay2_amount', 'pay2_date', 'pay3_amount', 'pay3_date')
        return Response(subscriptions)

    def post(self, request):
        content = {"res": request.data['hello']}
        return Response(content)

