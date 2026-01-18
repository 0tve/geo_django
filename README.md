Backend-приложение на Django для работы с географическими точками на карте. Приложение предоставляет REST API для создания точек, обмена сообщениями и поиска контента в заданном радиусе от указанных координат.

# Установка и запуск
1. Установить `GeoDjango / PostGIS` по инструкции: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install/
2. Создать базу данных на PostgreSQL и настроить конфигурацию в `settings.py`, следуя примеру в `settings.example.py` (константа `DATABASES`)
3. Выполнить миграции командой:
```
python.exe manage.py migrate
```
3. Запустить сервер:
```
python.exe manage.py runserver
```

### Устранение ошибок при установке
Если возникли ошибки с библиотекой `DGAL`, выполнить следующие шаги:
- Узнать текущую версию `GDAL` на вашей машине:
```
gdalinfo --version
```
- Удостовериться, что она не поддерживается https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install/geolibs/#geospatial-libraries
- Установить в ваше виртуальное окружение нужную версию https://github.com/cgohlke/geospatial-wheels/releases/tag/v2025.10.25 (например `gdal-3.11.4-cp314-cp314-win_amd64.whl`, где `3.11.4` - версия `GDAL`, а `cp` - версия `Python`, которая должна совпадать с вашей):
```
pip install path/to/file
```
- Добавить строку `GDAL_LIBRARY_PATH = r'<virtual_env_path>\Lib\site-packages\osgeo\gdal.dll'`

# Описание проекта
Стек: Python 3.14, Django 6, PostgreSQL, GeoDjango / PostGIS, Django Rest Framework (+ DRF-GIS), Django TestCase.

### Эндпоинты
1. POST `api/auth/register/` - создание пользователя
2. POST `api/auth/login/` - получение access-токена
3. POST `api/points/` - создание географической точки
4. GET `api/points/search/` - получение всех географических точек в заданном радиусе от точки
5. POST `api/points/{point_id}/messages/` - создание сообщения
6. GET `api/messages/search/` - получение сообщений в заданном радиусе от точки

Для доступа к эндпоинтам 3 и 5 необходимо передавать заголовок `Authorization: Token 'token'`. Токен можно получить при входе (2) или на этапе регистрации (1).

# Демонстрация работы в Postman
1. Регистрация пользователя
<img width="750" height="550" alt="reg" src="https://github.com/user-attachments/assets/a3e15bc5-3efc-4e9c-9e84-aed3802feb18" />

2. Вход в систему
<img width="750" height="550" alt="log" src="https://github.com/user-attachments/assets/67bbcd5b-d13a-48eb-bd8f-4d24e514d2db" />

3. Создание географической точки (Москва)
<img width="750" height="550" alt="1" src="https://github.com/user-attachments/assets/29c79520-7c27-4c49-b47d-c2a664ec7663" />

3.1 Неавторизованная попытка создать георафическую точку
<img width="750" height="550" alt="unauth" src="https://github.com/user-attachments/assets/000bd781-7972-4405-96d0-3197671c90d0" />

4. Создание сообщения в точке
<img width="750" height="550" alt="3" src="https://github.com/user-attachments/assets/a86e0258-d73a-437b-8764-da41062c9625" />

5. Получение географических точек в заданном радиусе (100) - отображается только Москва
<img width="750" height="800" alt="5" src="https://github.com/user-attachments/assets/c54a6d42-e629-4e64-a925-ec9788b53b12" />

5.1. Получение точек в большем радиусе (1000) - отображаются и Москва и Питер
<img width="750" height="950" alt="6" src="https://github.com/user-attachments/assets/fff76c0a-10c3-4b2a-a4e0-6aa1011f94cc" />

6. Валидация параметров
<img width="750" height="650" alt="7" src="https://github.com/user-attachments/assets/d70c37ed-f1e7-410c-a2e2-770330f9fb0e" />

7. Получение сообщений в заданном радиусе (100) - отображается только сообщение из Москвы
<img width="750" height="550" alt="8" src="https://github.com/user-attachments/assets/a04185b0-b8b5-44f3-897a-b93599dad628" />

7.1. Получение сообщений в большем радиусе (1000) - отображются сообщения из Москвы и Питера
<img width="750" height="600" alt="9" src="https://github.com/user-attachments/assets/c9ae349a-875e-40c6-a1a2-2c79077ed258" />
