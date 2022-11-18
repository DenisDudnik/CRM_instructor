# CRM_instructor
Портал объединяющий инструкторов и их клиентов

# Начальные настройки и действия для локального запука проекта
1. Из своей директории где вам удобно хранить репозитории выполните команду
   ```
   git clone git@github.com:DenisDudnik/CRM_instructor.git
   ```
   У вас появилась директория проекта

2. Перейдите в директорию проекта
   ```
   cd CRM_instructor
   ```

3. Создайте виртуальное окружение привычной вам командой. Например
   ```
   python3.9 -m venv venv
   ```

4. Активируйте виртуальное окружение. Для Linux:
   ```
   source venv/bin/activate
   ```

5. Установите зависимости командой
   ```
   pip install -r requirements/local.txt
   ```

6. Установите и активируйте проверку стиля кода командой
   ```
   pre-commit install
   ```
   Теперь при каждом commit’е утилиты будут проверять код по правилам и выдавать проблемные места, где нужно выполнить рефакторинг.
   Часть проблем будет исправляться автоматически. Нужно будет исправленные файлы снова добавить в commit и выполнить его повторно.

7. Создаем тома для данных
   ```
   docker volume create db_data_crm
   docker volume create redis_data
   docker volume create media_crm
   docker volume create django_static
   ```

8. Создаем ссылку на локальный файл с переменными окружения.
   При необходимости можно просто создать новый файл environment.
   ```
   ln -s environment.example environment
   ```

9.  Для локальной разработки нужен docker-compose.override.local.yaml
   нужно создать на него символьную ссылку:
   ```
   ln -s docker-compose.override.local.yaml docker-compose.override.yaml
   ```

* Далее вместо команды
  ```
  docker-compose
  ```
  возможно потребуется использовать команду (с пробелом вместо тире)
  ```
  docker compose
  ```

10. Теперь можно все собрать и запустить
   ```
   docker-compose up --build -d
   ```

11. Нужно создать пользователя
   ```
   docker-compose run --rm django ./manage.py createsuperuser
   ```

12. Сервер доступен по адресу:
    ```
    http://127.0.0.1:8000/
    http://127.0.0.1:8000/admin/
    ```
