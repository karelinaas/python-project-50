[![asciicast](https://asciinema.org/a/ihbUVumx9mVPHwjj.svg)](https://asciinema.org/a/ihbUVumx9mVPHwjj)

**Gendiff** - это утилита командной строки для сравнения двух конфигурационных файлов и отображения их различий. Программа поддерживает форматы файлов JSON и YAML и предоставляет несколько форматов вывода для удобного анализа изменений.

## Возможности

- Сравнение конфигурационных файлов в форматах JSON и YAML
- Три формата вывода:
  - `stylish` - форматированный иерархический вид (по умолчанию)
  - `plain` - текстовое описание изменений
  - `json` - формат JSON для программной обработки
- Поддержка вложенных структур
- Интерфейс командной строки с интуитивными аргументами
- Высокое покрытие тестами и качество кода

## Установка

### Предварительные требования

- Python 3.12 или выше
- [uv](https://docs.astral.sh/uv/) - современный менеджер пакетов Python

### Шаги установки

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/karelinaas/python-project-50.git
   cd python-project-50
   ```

2. **Установите зависимости:**
   ```bash
   make install
   # или
   uv sync
   ```

3. **Соберите и установите пакет:**
   ```bash
   make build
   make package-install
   ```

## Использование

### Базовый синтаксис

```bash
gendiff <first_file> <second_file> [-f FORMAT]
```

### Аргументы

- `first_file` - путь к первому файлу для сравнения
- `second_file` - путь ко второму файлу для сравнения
- `-f, --format` - формат вывода (stylish, plain, json). По умолчанию: stylish

### Примеры использования

#### Базовое сравнение (формат stylish)

```bash
gendiff file1.json file2.json
```

#### Сравнение с форматом plain

```bash
gendiff file1.json file2.json -f plain
```

#### Сравнение с выводом в JSON

```bash
gendiff file1.json file2.json -f json
```

#### Сравнение YAML файлов

```bash
gendiff config1.yml config2.yaml
```

#### Сравнение файлов разных форматов

```bash
gendiff config.json config.yml
```

### Форматы вывода

#### Формат stylish (по умолчанию)
```
{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}
```

#### Формат plain
```
Свойство 'follow' было удалено
Свойство 'proxy' было удалено  
Свойство 'timeout' было изменено. С '50' на '20'
Свойство 'verbose' было добавлено со значением: true
```

#### Формат JSON
```json
[{"key": "follow", "status": "removed", "value": false}, ...]
```

## Разработка

### Команды разработки

```bash
# Установка зависимостей
make install

# Запуск линтера
make lint

# Запуск тестов
uv run pytest

# Запуск тестов с покрытием
uv run pytest --cov=gendiff

# Сборка пакета
make build
```

### Тестирование

Проект имеет полное тестовое покрытие. Для запуска тестов:

```bash
# Все тесты
uv run pytest

# Конкретный тестовый файл
uv run pytest tests/test_diff.py

# С отчетом о покрытии
uv run pytest --cov=gendiff --cov-report=html
```

## Требования

- Python 3.12+
- PyYAML >= 6.0.0
- pytest >= 9.0.2 (для тестирования)
- ruff (для линтинга)

---

### Hexlet tests and linter status:
[![Actions Status](https://github.com/karelinaas/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/karelinaas/python-project-50/actions)

### Last build status:
[![Actions Status](https://github.com/karelinaas/python-project-50/actions/workflows/ci.yml/badge.svg)](https://github.com/karelinaas/python-project-50/actions)

### SonarQube status:
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=karelinaas_python-project-50&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=karelinaas_python-project-50)

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=karelinaas_python-project-50&metric=bugs)](https://sonarcloud.io/summary/new_code?id=karelinaas_python-project-50)

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=karelinaas_python-project-50&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=karelinaas_python-project-50)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=karelinaas_python-project-50&metric=coverage)](https://sonarcloud.io/summary/new_code?id=karelinaas_python-project-50)

[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=karelinaas_python-project-50&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=karelinaas_python-project-50)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=karelinaas_python-project-50&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=karelinaas_python-project-50)

[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=karelinaas_python-project-50&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=karelinaas_python-project-50)

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=karelinaas_python-project-50&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=karelinaas_python-project-50)

[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=karelinaas_python-project-50&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=karelinaas_python-project-50)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=karelinaas_python-project-50&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=karelinaas_python-project-50)

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=karelinaas_python-project-50&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=karelinaas_python-project-50)
