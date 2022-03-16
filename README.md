PASTA
============

https://pasta-petproject.ru/  

English version [below](#about).

О ПРОЕКТЕ
------------

Паста - веб-приложение, разработанное на веб-фреймворке Django языка Python для **учебных** и **демонстративных** целей. 
В приложении реализован функционал кулинарного сайта (кулинарной книги), с возможностью создания, редактирования, удаления собственных рецептов, 
а также добавления рецептов других пользователей в свою коллекцию избранных рецептов. Помимо этого пользователям доступен раздел "ВИКИ" 
с информацией о различных кулинарных ингредиентах и инструментах, используемых в процессе создания их шедевров.  
  
### Прочие возможности и функционал:  
- Регистрация с подтверждением эл. почты;
- Сброс пароля, используя эл. почту;
- Редактирование профиля пользователя (изменение фотографии, ФИ);
- Изменнение пароля пользователя;
- Навигация по собственным рецептам, используя фильтры по категориям (меню, кухня, публикация);
- Аналогичная навигация по избранным рецептам;
- Поиск рецептов, игредиентов, инструментов. 

### Программное обеспечение:  
- Python v3.8.10
- Django v4.0.2
- mysqlclient v2.1.0
- Pillow v9.0.1
- django-active-link v0.1.8
- pytils v0.3

УСТАНОВКА И НАСТРОЙКА
------------

### Настройка окружения

Перед началом работы рекомендую установить и настроить виртуальное окружение, 
используя [virtualenv](https://virtualenv.pypa.io/en/latest/) и [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).  
  
После настройки виртуального окружения клонируем репозиторий:  
    
    git clone https://github.com/alexhook/pasta_web.git

Переходим в директорию проекта и устанавливаем необходимые пакеты из файла requirements.txt:  
    
    cd pasta_web
    pip install -r requirements.txt --user

### Изменение настроек проекта

Далее открываем файл настроек settings.py:  
    
    nano pasta/pasta/settings.py

И изменяем следующие строки:  

    # settings.py
    ...
    SECRET_KEY = 'YOUR_SECRET_KEY'
    ...
    EMAIL_HOST = 'YOUR_EMAIL_HOST' # e.g. smtp.gmail.com
    EMAIL_HOST_USER = 'YOUR_EMAIL'
    EMAIL_HOST_PASSWORD = 'YOUR_EMAIL_PASSWORD'
    ...

### Установка и настройка MySQL

Если на вашем устройстве не установлен MySQL Server и MySQL Client, то переходим по [ссылке](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/) и производим его установку.  
  
Подключаемся к MySQL:  

    sudo mysql -u root

Создаем базу данных для нашего приложения:  

    CREATE DATABASE pasta;

Создаем пользователя, который будет использовать Django для доступа к БД ('user' и 'password' замените на собственные значения):  

    CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';

Даем права нашему пользователю на управдение ранее созданной БД ('user' заменить при необходимости):  

    GRANT ALL PRIVILEGES ON pasta.* TO 'user'@'localhost'
    
Для завершения работы обновляем права:  

    FLUSH PRIVILEGES;
    
Также советую установить пароль для root пользователя:  

    ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'new_password';

В завершение переходим в корневой каталог проекта (директория с файлом manage.py) и создаем файл .pasta.cnf, где указываем информацию, необходимую Django для подключения к БД:  

    cd pasta
    nano .pasta.cnf

Заполняем файл следующей информацией:  
    
    #.pasta.cnf
    
    [client]
    database = pasta
    user = user   # Замените на имя пользователя, которого вы создали
    password = password   # Замените на пароль, который вы указали ранее
    default-character-set = utf8

### Миграция и создания root пользователя

Находясь в корневом каталоге, производим миграцию моделей проекта в созданную БД:  

    python3 manage.py makemigrations
    python3 manage.py migrate
    
Создаем суперпользователя для доступа к административной панеле сайта. Следуя инструкциям скрипта, вводим логин, эл. адрес и пароль будущего пользователя:  

    python3 manage.py createsuperuser

### Завершающий этап

Наше приложение готово для использования на локальном сервере. Для запуска сервера вводим следующую команду:  

    python3 manage.py runserver
    
Сайт будет доступен по адресу http://127.0.0.1:8000/.  
  
  
  
  
  
  
  
  
  
  
  
  
ABOUT
------------

Pasta is a web application developed on the Django Python web framework for **educational** and **demonstrative** purposes.
The application implements the functionality of a culinary website (cookbook), with the ability to create, edit, delete your own recipes,
as well as add other users' recipes to your favorite collection. In addition, the WIKI section is available to users
with information about various culinary ingredients and tools used in the process of creating their masterpieces. 
  
### Other features and functionality:  
- Registration with email confirmation;
- Password reset using email;
- Editing the user profile (changing the photo, first and last names);
- Changing the user's password;
- Navigate your own recipes using filters by category (menu, cuisine, publication);
- Similar navigation to your favorites;
- Search for recipes, ingredients, tools. 

### Software:  
- Python v3.8.10
- Django v4.0.2
- mysqlclient v2.1.0
- Pillow v9.0.1
- django-active-link v0.1.8
- pytils v0.3

INSTALLATION AND CONFIGURATION
------------

### Setting up the virtualenv

Before starting work, I recommend installing and configuring a virtual environment,
using [virtualenv](https://virtualenv.pypa.io/en/latest/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).  
  
After setting up the virtual environment, clone the repository:  
    
    git clone https://github.com/alexhook/pasta_web.git

Go to the project directory and install the necessary packages from requirements.txt:  
    
    cd pasta_web
    pip install -r requirements.txt --user

### Changing Project settings

Open settings.py:  
    
    nano pasta/pasta/settings.py

And we change the following lines:  

    # settings.py
    ...
    SECRET_KEY = 'YOUR_SECRET_KEY'
    ...
    EMAIL_HOST = 'YOUR_EMAIL_HOST' # e.g. smtp.gmail.com
    EMAIL_HOST_USER = 'YOUR_EMAIL'
    EMAIL_HOST_PASSWORD = 'YOUR_EMAIL_PASSWORD'
    ...

### Installing and Configuring MySQL

If MySQL Server and MySQL Client are not installed on your computer, then click on [link](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/) 
and install it.  
  
Connecting to MySQL:  

    sudo mysql -u root

Creating a database for our application:  

    CREATE DATABASE pasta;

Creating a user who will use Django to access the database (replace 'user' and 'password' with your own values):  

    CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';

We grant privileges to our user to manage a previously created database (replace 'user' if necessary):  

    GRANT ALL PRIVILEGES ON pasta.* TO 'user'@'localhost'
    
To complete the work, we update the privileges:  

    FLUSH PRIVILEGES;
    
I also advise you to set a password for the root user:  

    ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'new_password';

At the end, go to the root directory of the project (with manage.py) and create a .pasta.conf file, 
where we specify the information necessary for Django to connect to the database:  

    cd pasta
    nano .pasta.cnf

Fill in the file with the following information:  
    
    #.pasta.cnf
    
    [client]
    database = pasta
    user = user   # Replace with the name of the user you created
    password = password   # Replace it with the password you specified earlier
    default-character-set = utf8

### Migration and creation of a root user

Being in the root directory, we migrate the project models to the created database:  

    python3 manage.py makemigrations
    python3 manage.py migrate
    
Creating a superuser to access the administrative panel of the site. 
Follow the instructions of the script and enter the login, email address and password of the future user:  

    python3 manage.py createsuperuser

### The final step

Our application is ready for use on a local server. To start the server, enter the following command:  

    python3 manage.py runserver
    
The site will be available at http://127.0.0.1:8000/.
