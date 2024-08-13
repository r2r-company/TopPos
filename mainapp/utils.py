from django.db.models import Sum

def get_stock_balance(nomenclature):
    # Відкладений імпорт для уникнення циклічного імпорту
    from .models import Opers

    # Сума товару за операцією "Прихід" (операція = 1)
    incoming = Opers.objects.filter(nomenclature=nomenclature, operation='1').aggregate(total=Sum('quantity'))['total'] or 0

    # Сума товару за операцією "Реалізація" (операція = 2)
    outgoing = Opers.objects.filter(nomenclature=nomenclature, operation='2').aggregate(total=Sum('quantity'))['total'] or 0

    # Різниця між приходом і реалізацією
    balance = incoming - outgoing
    return balance
