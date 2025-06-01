from rest_framework import serializers
from django import forms


errors = {}


def validate_cashflow_data(data, context='serializer', form_instance=None):
    amount = data.get('amount')
    category = data.get('category')
    subcategory = data.get('subcategory')
    type = data.get('type')

    # Валидация суммы
    if not amount:
        errors['amount'] = 'Укажите сумму'
    if amount <= 0:
        errors['amount'] = 'Сумма должна быть больше 0'

    # Валидация типа
    if not type:
        errors['type'] = 'Укажите тип ддс'

    # Валидация категории
    if not category:
        errors['category'] = 'Укажите категорию ддс'
    if category.type_id != type.id:
        errors['category'] = 'Категория не принадлежит выбранному типу'

    # Валидация подкатегории
    if not subcategory:
        errors['subcategory'] = 'Укажите подкатегорию ддс'
    if subcategory.category_id != category.id:
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
