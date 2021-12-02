from django.urls import path, re_path

from .views import FibView, LogView

urlpatterns = [
    re_path(r'^fib/?$', FibView.as_view()),
    re_path(r'^log/?$', LogView.as_view())
]
