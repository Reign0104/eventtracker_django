from django.urls import path
from .views import (
    PropListView, PropCreateView, PropUpdateView, PropDeleteView,
    borrower_list, borrower_add, borrower_edit,
    dashboard, use_prop, prop_use_history,
    # other imports...
)
from inventory.views import home 

urlpatterns = [
    path('', home, name='home'),

    path('props/', PropListView.as_view(), name='prop_list'),
    path('props/add/', PropCreateView.as_view(), name='prop_add'),
    path('props/<int:pk>/edit/', PropUpdateView.as_view(), name='prop_edit'),
    path('props/<int:pk>/delete/', PropDeleteView.as_view(), name='prop_delete'),

    path('borrowers/', borrower_list, name='borrower_list'),
    path('borrowers/add/', borrower_add, name='borrower_add'),
    path('borrowers/<int:borrower_id>/edit/', borrower_edit, name='borrower_edit'),

    path('dashboard/', dashboard, name='dashboard'),
    path('props/<int:prop_id>/use/', use_prop, name='use_prop'),
    path('props/<int:prop_id>/usage/', prop_use_history, name='prop_use_history'),

    # other URLs...
]
