
# LITESTARCATSCV

## NAME

**litestarcatscv** - тренировочный проект на кошках для освоения Litestar и других современных инструментов

## SYNOPSIS

`litestarcatscv [OPTIONS] [COMMAND]`

**Запуск через make:**

`make [run | test | check | format | db-migrate | db-upgrade | help]`

**Запуск напрямую:**

`uv run granian --interface asgi src/app:app`

## DESCRIPTION

**litestarcatscv** — это экспериментальный проект, созданный для изучения современных веб-фреймворков и инструментов разработки на Python. Основная цель — разработка простого API для создания и редактирования резюме (на кошках, разумеется), с использованием **Litestar**, **Granian**, **SQLAlchemy**, и других новомодных штук. Проект идеально подходит для тех, кто хочет попробовать что-то новое, не уходя в сложные рабочие задачи, и при этом получить удовольствие от пары вечеров за кодом.

Проект включает:

-   Карточку-резюме с опытом и навыками (кошачьими, естественно).
-   Возможность просмотра резюме по ссылке.
-   Редактирование и добавление информации.
-   Хранение данных в базе данных.

Тренируемся на кошках, потому что они милые и не жалуются на баги.

## OPTIONS

Проект управляется через Makefile. Доступные команды:

-   **run**
    Запускает сервер с приложением через Granian.
    Пример: make run
-   **test**
    Запускает тесты с использованием pytest.
    Пример: make test
-   **check**
    Проверяет код с помощью линтера Ruff.
    Пример: make check
-   **format**
    Автоматически форматирует код с помощью Ruff.
    Пример: make format
-   **revision**
    Создаёт новую миграцию базы данных через Alembic.
    Пример: make revision m="initial migration"
-   **upgrade**
    Применяет миграции к базе данных.
    Пример: make upgrade
 -  **downgrade**
    Отменяет применённые миграции
    Пример: make downgrade
-   **help**
    Показывает список доступных команд.
    Пример: make help

## ENVIRONMENT

Проект использует следующие инструменты и зависимости:

-   **Python 3.13.1** - интерпретатор, устанавливаемый через pyenv.
-   **Litestar** - ASGI-фреймворк для создания API.
-   **Granian** - высокопроизводительный сервер на Rust.
-   **SQLAlchemy** - ORM для работы с базой данных.
-   **Asyncpg** - асинхронный драйвер для PostgreSQL.
-   **Alembic** - инструмент миграций базы данных.
-   **KeyDB** - хранилище ключ-значение.
-   **Msgspec** - быстрая сериализация данных.
-   **UV** - менеджер зависимостей и виртуальных окружений.
-   **Direnv** - автоматическая загрузка окружения через .envrc.
-   **Ruff** - линтер и форматтер кода.
-   **Docker** - контейнеризация (в планах).
-   **Make** - автоматизация задач.

Для настройки окружения используется файл .envrc и .python-version.

## FILES

-   **src/app.py**
    Основной файл приложения Litestar.
-   **pyproject.toml**
    Конфигурация зависимостей и проекта.
-   **uv.lock**
    Lock-файл для фиксированных версий зависимостей.
-   **Makefile**
    Скрипт автоматизации задач.
-   **.envrc**
    Файл для настройки виртуального окружения через direnv.
-   **.python-version**
    Указывает версию Python для pyenv.

## INSTALLATION

1.  Установите зависимости системы (Ubuntu):

    `sudo apt update && sudo apt install -y build-essential libssl-dev zlib1g-dev \ libbz2-dev libreadline-dev libsqlite3-dev curl git \ libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev`

2.  Установите pyenv:

    `curl -fsSL https://pyenv.run | bash`

3.  Настройте shell (пример для zsh):

    `echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc source ~/.zshrc`

4.  Установите Python 3.13.1:

    `pyenv install 3.13.1`

5.  Установите direnv:

    `sudo apt-get install direnv echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc source ~/.zshrc`

6.  Установите uv:

    `curl -LsSf https://astral.sh/uv/install.sh | sh`

7.  Склонируйте репозиторий:

    `git clone <repository_url> cd litestarcatscv`

8.  Установите локальную версию Python:

    `pyenv local 3.13.1`

9.  Активируйте окружение:

    `direnv allow`

10.  Установите зависимости:
 `uv sync`


## EXAMPLES

Запуск сервера:

`make run`

Вывод:

`[INFO] Starting granian [INFO] Listening at: http://127.0.0.1:8000`

Проверка кода:

`make check`

Форматирование кода:

`make format`

## DIAGNOSTICS

-   **direnv: error .envrc is blocked**
    Выполните direnv allow для разрешения выполнения .envrc.
-   **uv: command not found**
    Убедитесь, что uv установлен и доступен в PATH.
-   **python: command not found**
    Проверьте, что pyenv настроен и версия Python установлена.

## BUGS

Сообщайте о багах в разделе Issues на GitHub или пишите в комментариях к статье на Хабре. Кошки тоже могут ошибаться! (У них лапки 🐾)

## AUTHOR

Написано мной. Тренируемся на кошках, чтобы потом покорять мир.

## SEE ALSO

**[litestar(1)](https://github.com/litestar-org/litestar)**, **[granian(1)](https://github.com/emmett-framework/granian)**, **[sqlalchemy(1)](https://github.com/sqlalchemy/sqlalchemy)**, **[uv(1)](https://github.com/astral-sh/uv)**, **[pyenv(1)](https://github.com/pyenv/pyenv)**, **[direnv(1)](https://github.com/direnv/direnv)**

Полный код(тут) и обсуждение: [Хабр статья 1](https://habr.com/ru/companies/ntechlab/articles/883578), [Хабр статья 2](https://habr.com/ru/companies/ntechlab/articles/889022/)
