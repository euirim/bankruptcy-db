from django.urls import path
from .views import CaseDetail

app_name = "cases"
urlpatterns = [
    path("<int:pk>/", view=CaseDetail.as_view(), name="detail"),
]
