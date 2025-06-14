# DDS Service — учёт движения денежных средств

Веб-приложение для создания, редактирования, просмотра и удаления записей о движении денежных средств (ДДС), с поддержкой логических зависимостей между сущностями и удобным HTML-интерфейсом.

## Используемые технологии

- Python 3.12
- Django 5.x
- Django REST Framework
- Django Filters
- Bootstrap (в кастомной HTML-админке)
- SQLite (по умолчанию, можно заменить на любую реляционную БД)

---

## Возможности

### Управление записями ДДС
- создание, редактирование, удаление и просмотр записей;
- поля: дата, статус, тип, категория, подкатегория, сумма, комментарий;
- ручной ввод даты (значение по умолчанию — сегодня);
- валидация на клиенте (на заполненность) и на сервере (на логическую согласованность);
- логические зависимости:
  - нельзя выбрать подкатегорию, не связанную с категорией;
  - нельзя выбрать категорию, не относящуюся к типу.

### Просмотр и фильтрация записей
- таблица записей с фильтрацией по:
  - периоду дат;
  - статусу;
  - типу;
  - категории;
  - подкатегории.

### Управление справочниками
- отдельный интерфейс для:
  - добавления, редактирования и удаления статусов, типов, категорий и подкатегорий;
- категории привязаны к типу;
- подкатегории привязаны к категории.

---

## Логика и валидация

- Валидация выполнена в одном месте (`validators.py`) и используется как в формах, так и в сериализаторах.
- Поля `тип`, `категория`, `подкатегория` и `сумма` обязательны. Валидация на стороне сервера и клиента.
- При ошибке выбора несовместимых категорий/типов/подкатегорий выдается понятное сообщение пользователю. Валидация на стороне сервера.

---

## Структура проекта
```
DDS-SERVICE/
├── core/  # Основное приложение (модели, формы, views и т.д.)
├──├─ admin.py  # Настройка Django-админки
├──├─ filters.py  # Django-filters для API и HTML
├──├─ forms.py  # Формы с Bootstrap и валидацией
├──├─ models.py  # Модели: статус, тип, категория, подкатегория, запись
├──├─ serializers.py  # DRF-сериализаторы
├──├─ urls.py  # Регистрация API и HTML маршрутов
├──├─ validators.py  # Общая серверная валидация данных
├──└─ views.py  # ViewSets и HTML-интерфейс
├── dds-service/  # Конфигурация Django-проекта (settings, urls)
├── manage.py
├── db.sqlite3  # SQLite база данных
├── requirements.txt  # Зависимости проекта
├── README.md
└── .gitignore
```

---

## Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/yourusername/dds-service.git
   cd dds-service
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # или venv\Scripts\activate на Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Примените миграции:**
   ```bash
   python manage.py migrate
   ```

5. **Запустите локальный сервер:**
   ```bash
   python manage.py runserver
   ```

6. **Откройте в браузере:**
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Статус соответствия ТЗ

| Требование | Статус |
|------------|--------|
| CRUD для записей ДДС | Выполнено |
| Справочники (статусы, типы, категории, подкатегории) | Выполнено |
| Поддержка связей между типом → категорией → подкатегорией | Выполнено |
| Валидация на клиенте и сервере | Выполнено |
| Фильтрация по всем параметрам | Выполнено |
| Простой, удобный интерфейс | Выполнено |
| Использование Django ORM и DRF | Выполнено |

---

## Автор

[Ксения Тетерчева](https://github.com/GreenVibesOnly) 🌿

Разработка выполнена в рамках тестового задания на позицию backend-разработчика.
