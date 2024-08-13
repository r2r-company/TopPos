from django.views.generic import ListView
from .models import Nomenclature

class NomenclatureListView(ListView):
    model = Nomenclature
    template_name = 'nomenclature_list.html'  # Використайте ваш шаблон
    context_object_name = 'nomenclatures'  # Ім'я контекстної змінної
