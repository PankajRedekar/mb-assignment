from django.conf.urls import url
from checkout import views

urlpatterns = [
    url('generate-hash-key/', views.GenerateHashKeyView.as_view(), name="generate-hash"),
    url('success/', views.SuccessView.as_view(), name="success"),
]