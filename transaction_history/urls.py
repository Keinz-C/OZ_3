from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.transaction_history_create, name="transaction_history_create"),
    path("list/", views.transaction_history_list, name="transaction_history_list"),
    # Add additional URL patterns for edit and delete views if needed
]
