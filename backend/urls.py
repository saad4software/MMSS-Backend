from django.urls import path
from backend import views
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', views.HelloView.as_view(), name='hello'),

    path('users/', views.UsersList.as_view()),
    path('users/new/', views.UsersCreate.as_view()),
    path('users/<int:id>/', views.UsersUpdate.as_view()),


    path('projects/', views.ProjectsList.as_view()),
    path('projects/new/', views.ProjectsCreate.as_view()),
    path('projects/<int:id>/', views.ProjectsUpdate.as_view()),

    path('spaces/', views.SpacesList.as_view()),
    path('spaces/new/', views.SpacesCreate.as_view()),
    path('spaces/<int:id>/', views.SpacesUpdate.as_view()),

    path('employees/', views.EmployeesList.as_view()),
    path('employees/new/', views.EmployeesCreate.as_view()),
    path('employees/<int:id>/', views.EmployeesUpdate.as_view()),

    path('motivations/', views.MotivationsList.as_view()),
    path('motivations/new/', views.MotivationsCreate.as_view()),
    path('motivations/<int:id>/', views.MotivationsUpdate.as_view()),

    path('ratios/', views.RatiosList.as_view()),
    path('ratios/new/', views.RatiosCreate.as_view()),
    path('ratios/<int:id>/', views.RatiosUpdate.as_view()),

    path('clients/', views.ClientsList.as_view()),
    path('clients/new/', views.ClientsCreate.as_view()),
    path('clients/<int:id>/', views.ClientUpdate.as_view()),

    path('subscriptions/', views.SubscriptionsList.as_view()),
    path('subscriptions/new/', views.SubscriptionCreate.as_view()),
    path('subscriptions/<int:id>/', views.SubscriptionUpdate.as_view()),

    path('payments/', views.PaymentList.as_view()),
    path('payments/new/', views.PaymentCreate.as_view()),
    path('payments/<int:id>/', views.PaymentUpdate.as_view()),

    path('transactions/', views.TransactionList.as_view()),
    path('transactions/new/', views.TransactionCreate.as_view()),
    path('transactions/<int:id>/', views.TransactionUpdate.as_view()),

    path('reports/salaries/', views.SalaryReport.as_view()),
    path('reports/subscriptions/', views.SubscriptionReport.as_view()),
    path('reports/notifications/', views.NotificationsReport.as_view()),
    path('reports/projects/', views.ProjectsReport.as_view()),
    path('reports/employees/', views.EmployeeReport.as_view()),

    path('reports/test', views.TimeSeriesView.as_view()),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
