from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Opers

@staff_member_required
def stock_report(request):
    # Отримуємо всі номенклатури
    nomenclatures = Opers.objects.values('nomenclature').distinct()

    # Формуємо дані для звіту
    report_data = []
    for nomenclature in nomenclatures:
        nomenclature_name = nomenclature['nomenclature']
        incoming = Opers.objects.filter(nomenclature=nomenclature_name, operation='1').aggregate(total=Sum('quantity'))['total'] or 0
        outgoing = Opers.objects.filter(nomenclature=nomenclature_name, operation='2').aggregate(total=Sum('quantity'))['total'] or 0
        balance = incoming - outgoing
        report_data.append({
            'nomenclature': nomenclature_name,
            'incoming': incoming,
            'outgoing': outgoing,
            'balance': balance
        })

    # Передаємо дані у шаблон
    context = {
        'report_data': report_data
    }
    return render(request, 'admin/stock_report.html', context)
