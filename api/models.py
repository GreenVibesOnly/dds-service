from datetime import date
from django.db import models


# Статусы
class Status(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)

    def __str__(self):
        return self.name


# Типы
class Type(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)

    def __str__(self):
        return self.name


# Категории, связанные с типом
class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    type = models.ForeignKey(Type,
                             on_delete=models.CASCADE,
                             related_name='categories',
                             verbose_name='Тип')

    def __str__(self):
        return self.name


# Подкатегории, связанные с категорией
class SubCategory(models.Model):
    name = models.CharField('Название', max_length=100)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='subcategories',
                                 verbose_name='Категория')

    def __str__(self):
        return self.name


# Запись о движении денежных средств (ДДС)
class CashflowRecord(models.Model):
    created_at = models.DateField('Дата создания', default=date.today)
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    status = models.ForeignKey(Status,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='cashflowrecord',
                               verbose_name='Статус')
    type = models.ForeignKey(Type,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='cashflowrecord',
                             verbose_name='Тип')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='cashflowrecord',
                                 verbose_name='Категория')
    subcategory = models.ForeignKey(SubCategory,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name='cashflowrecord',
                                    verbose_name='Подкатегория')
    comment = models.TextField('Комментарий', blank=True)

    def __str__(self):
        return f'{self.created_at} — {self.amount}₽'
