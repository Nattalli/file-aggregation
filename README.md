# Data aggregation test task

## Project Description

Даний проєкт є системою для завантаження, обробки та агрегації даних у форматах CSV та Excel. 
Проєкт дозволяє користувачам завантажувати файли, переглядати результати агрегації даних, 
а також адміністраторам управляти користувачами через систему реєстрації, логіну та виходу. 
Проєкт містить логування подій для відстеження активності користувачів та тести для забезпечення перевірки валідності 
функціоналу при змінах.

## Key Features

1. **User registration and authentication:**
  - реєстрація нових користувачів.
  - аутентифікація користувачів з можливістю входу та виходу з системи.

2. **File upload:**
  - підтримка завантаження файлів у форматах CSV та Excel.
  - перевірка наявності необхідних колонок та валідація формату даних.
  - обробка даних з логуванням помилок.

3. **Data aggregation:**
  - агрегація даних за різними критеріями: місяцями, платформами, брендами та рекламодавцями.
  - підрахунок середніх значень для аналізу показів.

4.  **Data visualization:**
візуалізація агрегованих даних у вигляді графіків (стовпчасті діаграми, кільцеві діаграми) за допомогою Chart.js.

5. **Error logging:**
  - логування  дій користувачів, зокрема помилок під час завантаження та обробки файлів.
  - логи зберігаються в базі даних, можна переглянути їх через адмін-панель.

6. **User roles and permissions:**
вбудована підтримка різних ролей користувачів (користувач та адміністратор).

7. **Admin dashboard:**
адміністративна панель для управління користувачами, перегляду логів та управління файлами.

8. **Testing:**
набір тестів для  основних компонентів системи, включаючи форми, в'юшки та утиліти.

## Functionality

- **Реєстрація:** користувачі можуть зареєструватися за допомогою форми реєстрації.
- **Логін/Логаут:** вхід в систему здійснюється через форму логіну, вихід — через відповідну кнопку.
- **Завантаження файлів:** увійшовши в систему, користувач може завантажити CSV або Excel файли для обробки та агрегації даних.
- **Агреговані результати:** після завантаження та обробки файлу користувач може переглянути агреговані результати у вигляді таблиць і графіків.
- **Логування подій:** усі дії користувачів, такі як завантаження файлів та помилки, логуються.

## Project overview

### 1. Реєстрація

![registration.png](readme-media%2Fregistration.png)

### 2. Логін

![login.png](readme-media%2Flogin.png)

### 3. Завантаження не валідного файлу

![upload_invalid_file_2.png](readme-media%2Fupload_invalid_file_2.png)
![upload_invalid_file.png](readme-media%2Fupload_invalid_file.png)

### 4. Завантаження валідного файлу

![upload_file.png](readme-media%2Fupload_file.png)

### 5. Дашборд з агрегованими даними

![dashboard_1.png](readme-media%2Fdashboard_1.png)
![dashboard_2.png](readme-media%2Fdashboard_2.png)
![dashboard_3.png](readme-media%2Fdashboard_3.png)
![dashboard_4.png](readme-media%2Fdashboard_4.png)

### 6. Вхід в адміністративну панель звичайним користувачем

![admin_panel_login_via_user.png](readme-media%2Fadmin_panel_login_via_user.png)

### 7. Адміністративна панелі

![admin_table.png](readme-media%2Fadmin_table.png)
![admin_users_ibfo.png](readme-media%2Fadmin_users_ibfo.png)
![admin_logs.png](readme-media%2Fadmin_logs.png)
![admin_files_upload.png](readme-media%2Fadmin_files_upload.png)

## Testing

Проєкт містить тести для форм, в'юшок та утиліт. Для запуску тестів:

```bash
pytest
```

Результати тестування

![tests.png](readme-media%2Ftests.png)

## Installation using Github

Python 3.10+ is a must

1. Clone the repository in the terminal:
`git clone https://github.com/Nattalli/file-aggregation.git`
2. Create virtual env:
`python -m venv venv`
3. Setup virtual env:
    * On Windows: `venv\Scripts\activate`
    * On Linux or MacOS: `source venv/bin/activate`
4. Go to the `datascientist_testtask` folder: `datascientist_testtask`
5. And mark it as the source root 
6. Install requirements: `pip install -r requirements.txt`
7. Make migrations: `python manage.py migrate`
8. Now you can run it: `python manage.py runserver`
9. You can create superuser for testing admin functionality with following command:
`python manage.py createsuperuser`
