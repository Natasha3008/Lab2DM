# Lab2DM
2nd lab DM
# Hotel Database Management Application

## 1. Введение
В этом проекте разработано приложение для управления базой данных отелей на языке программирования Python с использованием библиотеки SQLite. 

### Краткое описание предметной области

В отелях обычно существует несколько классов номеров (эконом, стандарт, комфорт, люкс и т.д.). У каждого номера есть уникальный номер и характеристики, такие как цена, количество комнат и наличие удобств (wi-fi, кондиционер, холодильник и т.д.). Также необходимо знать статус номера (занят, свободен, на брони).

#### Атрибуты:
- **Room_ID**: для нумерации номеров отеля.
- **Room_Type**: класс номера.
- **Price**: стоимость номера.
- **Room_Count**: количество доступных комнат данного типа.
- **Amenities**: перечень удобств, имеющихся в номере.
- **Status**: статус номера (занят/свободен/на брони).

Разработанное приложение может выполнять следующие функции: добавлять, обновлять, удалять и искать записи о номерах, а также экспортировать и импортировать данные из CSV файлов.

---

## 2. Описание предметной области БД
База данных для управления отелями содержит следующие сущности:

### Tables

- **Rooms**: таблица, содержащая информацию о гостиничных номерах. Каждый номер имеет:
  - **Room_ID**: уникальный идентификатор (строка).
  - **Room_Type**: тип номера (строка).
  - **Price**: цена номера за ночь (число с плавающей запятой).
  - **Room_Count**: общее количество доступных номеров данного типа (целое число).
  - **Amenities**: список доступных удобств в номере (строка).
  - **Status**: статус номера (строка).

---

## 3. Временная статистика и анализ сложности-эффективности алгоритмов

P.S. Я очень старалась добиться либо константной, либо логарифмической сложности.

### 3.1 Добавление записи в БД
- **Метод**: `add_record()`
- **Алгоритм**: SQL-запрос и кортеж для передачи параметров в SQL-запрос.
- **Сложность**: Проверка существования: **O(1)** – использование индекса по Room_ID.

### 3.2 Удаление записи из БД
- **Метод**: `delete_record()`
- **Алгоритм**: Удаление записи по Room_ID.
- **Сложность**: **O(log n)** – при использовании индексов для ускорения поиска записи перед удалением.

### 3.3 Поиск по БД
- **Метод**: `search_records()`
- **Алгоритм**: Поиск записи по Room_ID.
- **Сложность**: **O(1)**.
