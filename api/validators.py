from rest_framework import serializers
from django import forms


def validate_cashflow_data(data, context='serializer', form_instance=None):
    errors = {}

    amount = data.get('amount')
    category = data.get('category')
    subcategory = data.get('subcategory')
    type = data.get('type')

    # Валидация суммы
    if not amount:
        errors['amount'] = 'Укажите сумму'
    elif amount <= 0:
        errors['amount'] = 'Сумма должна быть больше 0'

    # Валидация типа, категории и подкатегории
    if not subcategory:
        errors['subcategory'] = 'Укажите подкатегорию ддс'
    elif not category:
        errors['category'] = 'Укажите категорию ддс'
    elif not type:
        errors['type'] = 'Укажите тип ддс'
    elif category.type_id != type.id:
        errors['category'] = 'Категория не принадлежит выбранному типу'
    elif subcategory.category_id != category.id:
        errors['subcategory'] = (
            'Подкатегория не принадлежит выбранной категории'
        )

    if errors:
        if context == 'serializer':
            raise serializers.ValidationError(errors)
        elif context == 'form' and form_instance is not None:
            for field, message in errors.items():
                form_instance.add_error(field, message)
            raise forms.ValidationError('Проверьте заполнение формы.')
        else:
            raise Exception('Неизвестная ошибка при валидации формы')

    return data
