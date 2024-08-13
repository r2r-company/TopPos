from django.urls import path
from . import views

urlpatterns = [
    path('nomenclature/', views.NomenclatureListView.as_view(), name='nomenclature_list'),

]
