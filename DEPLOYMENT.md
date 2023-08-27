# Deployment

### 1. Setting up the database
- Log in to ElephantSQL.com to access your dashboard.
- Click on "Create New Instance".
- Set up your plan:
  - Give your plan a Name (usually the project's name).
  - Select the Tiny Turtle (Free) plan.
  - Tags field can be left blank.
- Select "Select Region":
  - Choose a data center near your location.
  - If the chosen data center is not available, pick another.
- Click "Review", verify your details, and then click "Create Instance".
- Return to the ElephantSQL dashboard and click on the database instance name for this project.
- In the URL section, click the copy icon to copy the database URL to your clipboard.

### 2. Creating the Heroku app
1. Log into Heroku and Access the Dashboard
2. Once you're logged in click on "New" to start creating a new app.
    - You will need to provide a unique name for your app
    - Then select the region that's closest to you
    - Once done, click "Create app" to confirm
3. In your new app, navigate to the "Settings" tab
    - In your settings click "Reveal Config Vars"
    - Add a config var named **DATABASE_URL** 
    - For the value, past in the database URL from the instance you created on ElephantSQL.com
    - **PLEASE NOTE:** Do not put quotation marks around your database URL string


### 3. Connect our project to ElephantSQL database
1. In the terminal in you development environment, install **dj_databaseurl** and **psycopg2**
  ```
  pip3 install dj_database_url==0.50 psycopg2
  ```
2. Update your requirements.txt file
  ```
  pip freeze > requirements.txt
  ```
3. In your **settings.py** file import dj_database_url underneath the import for os
  ``` 
  import os
  import dj_database_url
  ```
4. Remaining in your settings.py file scroll to the **DATABASES** section and comment out the sqlite3 database and connect to your ElephantSQL database URL. Your code should look like this:
  ```
  # DATABASES = {
  #     'default': {
  #         'ENGINE': 'django.db.backends.sqlite3',
  #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  #     }
  # }
     
  DATABASES = {
      'default': dj_database_url.parse('your-database-url-here')
  }
  ```
5. In the terminal, run the showmigrations command to confirm that you are connected to the database. You should see a list of migrations but none of them will be checked off.
  ```
  python manage.py showmigrations
  ```
6. Then, migrate your database models to your new database with the following command:
  ```
  python3 manage.py migrate
  ```
7. Once you have migrated you will need to create a superuser with the following command:
  ```
  python3 manage.py createsuperuser
  ```
8. Follow the steps to create your superuser username and password. The email address can be left blank.
9. To prevent exposing our database when pushed to github you  need to delete it from the settings.py file. This will be set up later. Once deleted your database setting should look like this:
```
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
      }
  }
```

### 4. Confirming the database is set up
1. Navigate to your ElephantSQL database page.
2. On the left of the page select "BROWSER"
3. From here, click the Table queries button and select "auth_user"
4. When you click "Excecute" you should see your newly created superuser. This confirms that your tables have been created and you can add to your database.


### 5. Deploying to herkou
1. Write an if statement around your database variables. So that when connected to Heroku the app will use the postgres database otherwise it connect to SQLite.
```
  if 'DATABASE_URL' in os.environ:
      DATABASES = {
          'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
      }
  else:
      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.sqlite3',
              'NAME': BASE_DIR / 'db.sqlite3',
          }
      }
```
2. Install gunicorn to act as your web server. In the terminal type the following command:
```
  pip3 install gunicorn
```
3. Freeze the requirements in the terminal:
```
  pip3 freeze > requirements.txt
```
4. Create a file name Procfile in the root directory. This tells Heroku to create a web dyno which will run gunicorn and serve our Django app. in the file you will need to include the following line:
```
  web: gunicorn fizzybeese.wsgi:application
```
5. Log into Heroku and navigate to the config vars in the settings tab of your app. Add the config variable **DISABLE_COLLECTSTATIC** to **1**
6. While on Heroku you can connect to your GitHub repository by going to the "Deploy" tab. Under the heading "Deployment Method" select GitHub. Once connected, under the heading "App connected to GitHub" select the relevant repository.
7. Back in your project's settings.py file, add your Heroku app to the allowed hosts. This will be in the settings tab under the "Domains" heading. You can add 'localhost' here also to allow you it to still work in Gitpod. Your ALLOWED_HOSTS should look something like this.
```
  ALLOWED_HOSTS = ['fizzybeese-52707759b9ba.herokuapp.com', 'localhost']
```


8. You can then attempt to deploy our app by adding and commiting our changes.

 





