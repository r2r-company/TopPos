from django.urls import path
from django.contrib.admin import AdminSite, TabularInline, ModelAdmin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import (
    Country, Manufacturer, Supplier, MeasurementUnit,
    NomenclatureGroup, PriceType, NomenclatureType,
    NomenclatureStatus, Nomenclature, Company, Warehouse, Workshop,
    GoodsReceipt, GoodsReceiptItem, GoodsIssue, GoodsIssueItem, Opers
)
from django.db.models import Sum

# Реєстрація моделей
class NomenclatureAdmin(ModelAdmin):
    list_display = ('name', 'type', 'article', 'status', 'supplier')
    search_fields = ('name', 'article', 'barcode')
    list_filter = ('type', 'status', 'group', 'country_of_origin', 'manufacturer', 'supplier')

class CompanyAdmin(ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email')
    search_fields = ('name', 'address')

class WarehouseAdmin(ModelAdmin):
    list_display = ('name', 'company', 'location')
    search_fields = ('name', 'location')
    list_filter = ('company',)

class WorkshopAdmin(ModelAdmin):
    list_display = ('name', 'company', 'location')
    search_fields = ('name', 'location')
    list_filter = ('company',)

class OpersAdmin(ModelAdmin):
    list_display = ('nomenclature', 'operation', 'company', 'warehouse', 'workshop', 'date', 'time', 'document_number')
    search_fields = ('nomenclature', 'document_number')
    list_filter = ('operation', 'company', 'date')


class GoodsReceiptItemInline(TabularInline):
    model = GoodsReceiptItem
    extra = 1  # Кількість пустих рядків для заповнення

class GoodsReceiptAdmin(ModelAdmin):
    list_display = ('company', 'supplier', 'date_time')
    inlines = [GoodsReceiptItemInline]

class GoodsIssueItemInline(TabularInline):
    model = GoodsIssueItem
    extra = 1  # Кількість пустих рядків для заповнення

class GoodsIssueAdmin(ModelAdmin):
    list_display = ('company', 'customer', 'date_time')
    inlines = [GoodsIssueItemInline]


class MyAdminSite(AdminSite):
    site_header = 'TopPos'
    site_title = 'Адмін панель'
    index_title = 'Управління'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('stock-report/', self.admin_view(stock_report), name='stock_report'),
        ]
        return custom_urls + urls

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_reports'] = [
            {
                'name': 'Звіт про залишки товару',
                'url': 'stock-report/'
            }
        ]
        return super().index(request, extra_context)

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request)
        for app in app_list:
            if app['name'] == 'Mainapp':  # Використовуйте назву вашого додатка
                order = [
                    'Компанії', 'Склади', 'Цехи', 'Номенклатури', 'Виробники', 'Постачальники',
                    'Поступлення товару', 'Реалізації товару', 'Групи номенклатури',
                    'Одиниці виміру', 'Типи номенклатури', 'Ціни', 'Статуси номенклатури'
                ]
                app['models'].sort(key=lambda x: order.index(x['name']) if x['name'] in order else len(order))
        return app_list


# Сигнал для створення записів в Opers при збереженні GoodsReceiptItem
@receiver(post_save, sender=GoodsReceiptItem)
def create_opers_for_goods_receipt(sender, instance, created, **kwargs):
    if created:
        Opers.objects.create(
            nomenclature=instance.nomenclature.name,
            purchase_price=instance.purchase_price,
            selling_price=None,  # Для приходу товару ціна продажу не заповнюється
            quantity=instance.quantity,  # Заповнюється кількість
            company=instance.goods_receipt.company.name,
            warehouse=None,  # Тут можна вказати відповідне поле, якщо є
            workshop=None,  # Тут можна вказати відповідне поле, якщо є
            date=instance.goods_receipt.date_time.date(),
            time=instance.goods_receipt.date_time.time(),
            document_number=instance.goods_receipt.id,  # Використовуйте реальний номер документа
            operation='1'  # Прихід товару
        )

# Сигнал для створення записів в Opers при збереженні GoodsIssueItem
@receiver(post_save, sender=GoodsIssueItem)
def create_opers_for_goods_issue(sender, instance, created, **kwargs):
    if created:
        Opers.objects.create(
            nomenclature=instance.nomenclature.name,
            purchase_price=None,  # Для реалізації товару ціна закупу не заповнюється
            selling_price=instance.selling_price,
            quantity=instance.quantity,  # Заповнюється кількість
            company=instance.goods_issue.company.name,
            warehouse=None,  # Тут можна вказати відповідне поле, якщо є
            workshop=None,  # Тут можна вказати відповідне поле, якщо є
            date=instance.goods_issue.date_time.date(),
            time=instance.goods_issue.date_time.time(),
            document_number=instance.goods_issue.id,  # Використовуйте реальний номер документа
            operation='2'  # Реалізація товару
        )


# Реєстрація моделей у кастомній адмін панелі
admin_site = MyAdminSite(name='myadmin')
admin_site.register(Company, CompanyAdmin)
admin_site.register(Warehouse, WarehouseAdmin)
admin_site.register(Workshop, WorkshopAdmin)
admin_site.register(Nomenclature, NomenclatureAdmin)
admin_site.register(Manufacturer)
admin_site.register(Supplier)
admin_site.register(GoodsReceipt, GoodsReceiptAdmin)
admin_site.register(GoodsIssue, GoodsIssueAdmin)
admin_site.register(Opers, OpersAdmin)
admin_site.register(Country)
admin_site.register(MeasurementUnit)
admin_site.register(NomenclatureGroup)
admin_site.register(PriceType)
admin_site.register(NomenclatureType)
admin_site.register(NomenclatureStatus)


# Кастомний view для звіту про залишки товару
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
