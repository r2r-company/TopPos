from django.core.exceptions import ValidationError
from django.db import models
from .utils import get_stock_balance



from mainapp.utils import get_stock_balance


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва країни")

    class Meta:
        verbose_name = "Країна"
        verbose_name_plural = "Країни"

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва виробника")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name="Країна")

    class Meta:
        verbose_name = "Виробник"
        verbose_name_plural = "Виробники"

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name="Постачальник")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name="Країна")

    class Meta:
        verbose_name = "Постачальник"
        verbose_name_plural = "Постачальники"

    def __str__(self):
        return self.name

class MeasurementUnit(models.Model):
    name = models.CharField(max_length=50, verbose_name="Одиниця виміру")
    abbreviation = models.CharField(max_length=10, verbose_name="Скорочення")

    class Meta:
        verbose_name = "Одиниця виміру"
        verbose_name_plural = "Одиниці виміру"

    def __str__(self):
        return self.name

class NomenclatureGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Група номенклатури")

    class Meta:
        verbose_name = "Група номенклатури"
        verbose_name_plural = "Групи номенклатури"

    def __str__(self):
        return self.name

class PriceType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип ціни")

    class Meta:
        verbose_name = "Тип ціни"
        verbose_name_plural = "Типи цін"

    def __str__(self):
        return self.name

class NomenclatureType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип номенклатури")

    class Meta:
        verbose_name = "Тип номенклатури"
        verbose_name_plural = "Типи номенклатури"

    def __str__(self):
        return self.name

class NomenclatureStatus(models.Model):
    status = models.CharField(max_length=50, verbose_name="Статус номенклатури")

    class Meta:
        verbose_name = "Статус номенклатури"
        verbose_name_plural = "Статуси номенклатури"

    def __str__(self):
        return self.status



class Nomenclature(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва номенклатури")
    type = models.ForeignKey(NomenclatureType, on_delete=models.SET_NULL, null=True, verbose_name="Тип номенклатури")
    article = models.CharField(max_length=100, unique=True, verbose_name="Артикул", blank=True, null=True)
    measurement_unit = models.ForeignKey(MeasurementUnit, related_name='measurement_unit', on_delete=models.SET_NULL, null=True, verbose_name="Одиниця виміру")
    base_measurement_unit = models.ForeignKey(MeasurementUnit, related_name='base_measurement_unit', on_delete=models.SET_NULL, null=True, verbose_name="Базова одиниця виміру")
    barcode = models.CharField(max_length=50, blank=True, null=True, verbose_name="Штрих-код")
    country_of_origin = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name="Країна походження")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, verbose_name="Виробник")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    image = models.ImageField(upload_to='nomenclature_images/', blank=True, null=True, verbose_name="Зображення")
    group = models.ForeignKey(NomenclatureGroup, on_delete=models.SET_NULL, null=True, verbose_name="Група номенклатури")
    warehouse_unit = models.ForeignKey(MeasurementUnit, related_name='warehouse_unit', on_delete=models.SET_NULL, null=True, verbose_name="Складська одиниця")
    min_stock = models.PositiveIntegerField(default=0, verbose_name="Мінімальний залишок", blank=True, null=True)
    max_stock = models.PositiveIntegerField(default=0, verbose_name="Максимальний залишок", blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Знижка", blank=True, null=True)
    external_system_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Код для зовнішньої системи")
    characteristics = models.JSONField(blank=True, null=True, verbose_name="Характеристика номенклатури")
    status = models.ForeignKey(NomenclatureStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Статус номенклатури")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Постачальник")

    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатури"

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва компанії")
    address = models.CharField(max_length=255, verbose_name="Адреса компанії", blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name="Телефонний номер", blank=True, null=True)
    email = models.EmailField(verbose_name="Електронна пошта", blank=True, null=True)

    class Meta:
        verbose_name = "Компанія"
        verbose_name_plural = "Компанії"

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва складу")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='warehouses', verbose_name="Компанія")
    location = models.CharField(max_length=255, verbose_name="Розташування", blank=True, null=True)

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склади"

    def __str__(self):
        return self.name


class Workshop(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва цеху")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='workshops', verbose_name="Компанія")
    location = models.CharField(max_length=255, verbose_name="Розташування", blank=True, null=True)

    class Meta:
        verbose_name = "Цех"
        verbose_name_plural = "Цехи"

    def __str__(self):
        return self.name


class GoodsReceipt(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компанія")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="Постачальник")
    date_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата та час")

    class Meta:
        verbose_name = "Поступлення товару"
        verbose_name_plural = "Поступлення товару"

    def __str__(self):
        return f"Поступлення від {self.supplier.name} до {self.company.name} на {self.date_time}"


class GoodsReceiptItem(models.Model):
    goods_receipt = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name='items')
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.CASCADE, verbose_name="Номенклатура")
    quantity = models.PositiveIntegerField(verbose_name="Кількість")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна закупівлі")

    class Meta:
        verbose_name = "Позиція поступлення"
        verbose_name_plural = "Позиції поступлення"

    def __str__(self):
        return f"{self.nomenclature.name} - {self.quantity} шт. за {self.purchase_price} грн"


class GoodsIssue(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компанія")
    customer = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="Покупець")  # Можливо, вам потрібна модель для клієнта
    date_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата та час")

    class Meta:
        verbose_name = "Реалізація товару"
        verbose_name_plural = "Реалізації товару"

    def __str__(self):
        return f"Реалізація до {self.customer.name} від {self.company.name} на {self.date_time}"


class GoodsIssueItem(models.Model):
    goods_issue = models.ForeignKey(GoodsIssue, on_delete=models.CASCADE, related_name='items')
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.CASCADE, verbose_name="Номенклатура")
    quantity = models.PositiveIntegerField(verbose_name="Кількість")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна продажу")

    class Meta:
        verbose_name = "Позиція реалізації"
        verbose_name_plural = "Позиції реалізації"

    def clean(self):
        # Підрахунок залишку товару
        stock_balance = get_stock_balance(self.nomenclature)

        if self.quantity > stock_balance:
            raise ValidationError(
                f"Недостатньо товару {self.nomenclature.name} на складі. Доступно: {stock_balance}, запитано: {self.quantity}")

    def save(self, *args, **kwargs):
        self.clean()  # Перевірка перед збереженням
        super().save(*args, **kwargs)




class Opers(models.Model):
    NOMENCLATURE_CHOICES = [
        ('1', 'Прихід товару'),
        ('2', 'Реалізація товару'),
        ('3', 'Списання товару'),
    ]

    nomenclature = models.CharField(max_length=200, verbose_name="Номенклатура")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна закупу", null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна продажу", null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name="Кількість", null=True, blank=True)
    company = models.CharField(max_length=200, verbose_name="Компанія", null=True, blank=True)
    warehouse = models.CharField(max_length=200, verbose_name="Склад", null=True, blank=True)
    workshop = models.CharField(max_length=200, verbose_name="Цех", null=True, blank=True)
    date = models.DateField(verbose_name="Дата", null=True, blank=True)
    time = models.TimeField(verbose_name="Година", null=True, blank=True)
    document_number = models.CharField(max_length=50, verbose_name="Номер документа", null=True, blank=True)
    operation = models.CharField(max_length=1, choices=NOMENCLATURE_CHOICES, verbose_name="Операція")

    class Meta:
        verbose_name = "Операція"
        verbose_name_plural = "Операції"

    def __str__(self):
        return f"{self.nomenclature} - {self.get_operation_display()}"