from django.urls import path
from .views import CreateCompanyView

urlpatterns = [
    path('create/', CreateCompanyView.as_view(), name='create-company'),
    # path('<int:company_id>/create-car/', CreateCarView.as_view(), name='create-car'),

]