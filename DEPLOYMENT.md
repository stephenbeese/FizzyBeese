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


### 3. Connect our project to the ElephantSQL database
1. In the terminal in your development environment, install **dj_databaseurl** and **psycopg2**
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

4. Remaining in your settings.py file scroll to the **DATABASES** section, comment out the SQLite3 database and connect to your ElephantSQL database URL. Your code should look like this:
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

9. To prevent exposing our database when pushed to Github you need to delete it from the settings.py file. This will be set up later. Once deleted your database setting should look like this:
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

4. When you click "Execute" you should see your newly created superuser. This confirms that your tables have been created and you can add them to your database.


### 5. Deploying to Heroku
1. Write an if statement around your database variables. So that when connected to Heroku the app will use the PostgreSQL database otherwise it connects to SQLite.
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

4. Create a file named Procfile in the root directory. This tells Heroku to create a web dyno that will run gunicorn and serve our Django app. In the file you will need to include the following line:
```
  web: gunicorn fizzybeese.wsgi:application
```

5. Log into Heroku and navigate to the config vars in the settings tab of your app. Add the config variable **DISABLE_COLLECTSTATIC** to **1**

6. While on Heroku you can connect to your GitHub repository by going to the "Deploy" tab. Under the heading "Deployment Method" select GitHub. Once connected, under the heading "App connected to GitHub" select the relevant repository. Then click on "Enable Automatic Deploys".

7. Back in your project's settings.py file, add your Heroku app to the allowed hosts. This will be in the settings tab under the "Domains" heading. You can add 'localhost' here also to allow it to still work in Gitpod. Your ALLOWED_HOSTS should look something like this.
```
  ALLOWED_HOSTS = ['fizzybeese-52707759b9ba.herokuapp.com', 'localhost']
```

8. You can then attempt to deploy our app by adding and committing our changes and pushing them to GitHub.

9. Once pushed to GitHub you can view the build log of the app under the "Activity" tab on your Heroku app page.

10. If this builds correctly you will be able to view the app by the link at the bottom of the build log or the "Open app" button at the top of the page.

11. Once you have confirmed your app is working, find a Django secret key generator online and copy a new key to your clipboard. In your config vars section in your Heroku app add the config variable **SECRET_KEY** with the value you have just copied.

12. In your settings.py file change the secret key to get it from the environment variables. By typing the following:
```
  SECRET_KEY = os.environ.get('SECRET_KEY', '')
```
and in your env.py file add the following line:
```
  os.environ["SECRET_KEY"] = "your-secret-key"
```
ensuring it is the same value as is in your config variables.

13. Once you have done this you can now add, commit, and push to GitHub.

### 5. Connecting to AWS
1. First, navigate to aws.amazon.com and log in or create an account.
  - If you do not have an account follow these steps:
    - Fill out your email address, choose a password and an account name, and click continue.
    - Choose an account type of personal and then enter your required details.
    - You will be asked to enter your credit/debit card details for billing in case you go over the free usage limit.
    - You will then need to click through a few more things to register your account.

2. Once your account has been registered, go back to aws.amazon.com, click on the "My Account" dropdown menu, and go to "AWS Management Console"

3. From here search for "S3" in the search bar or find it through the services menu. In the S3 menu create a new bucket.

4. In the S3 menu create a new bucket, this will be used to store your files. To set up the bucket follow these steps:
    - Name the bucket the same as your Heroku project name. You can name it anything but naming it the same keeps everything organised.
    - If you're asked to select a region, select the one closest to you.
    - Under "Object Ownership" select the box that says ACLs enabled and ensure that Bucket ownership preferred is selected below.
    - You'll also want to uncheck "Block all public access" and check the box to say that you acknowledge the bucket is public.
    - The remaining settings can be left default.
    - Click on Create Bucket.

5. You now need to change some settings in the bucket.
    - First, click on your newly created bucket go to the properties tab, and scroll to the bottom.
    - From here you will find a section that says static website hosting. Click on the edit button. 
    - Then, select Enable, and in the index and error document text boxes enter ``` index.html ``` and ``` error.html ``` respectively.
    - Click Save changes.
    - Navigate to the permissions tab and scroll to the Cross-origin resource sharing (CORS) section. 
      - This is going to set up the required access between our Heroku app and this S3 bucket
      - Click edit and paste in the following:
    ```
      [
        {
          "AllowedHeaders": [
            "Authorization"
          ],
          "AllowedMethods": [
            "GET"
          ],
          "AllowedOrigins": [
            "*"
          ],
          "ExposeHeaders": []
        }
      ]
    ```
      This is going to set up the required access between our Heroku app and this S3 bucket
    - Scroll up to bucket policy and again click edit. From here click Policy Generator and follow these steps:
      - Select a policy type of S3 Bucket Policy
      - Allow all principals by using an asterisk *
      - Then under the Actions section select GetObject
      - From the bucket policy tab copy your Amazon Resource Name (ARN) and paste it in the ARN text box at the bottom of the policy generator
      - Click Add Statement
      - Click Generate Policy
      - Then copy the policy and add it to the bucket policy editor.
      - Before you click save add ```/*``` to the end of the resource key.
      - Now you can click Save Changes.
    - On the bucket policy section scroll down to the Access Control List (ACL) section and click edit.
      - On this page enable List for Everyone (public access) accept the warning box and click save

### 6. Creating AWS Groups, Policies, and Users
  1. Create a new group by following these steps:
  - Back in the services menu search or find the IAM section.
  - From the IAM dashboard click on User Groups and then click on Create Group.
  - Create a meaningful name for your group. Generally, something that makes sense, such as ```manage-your-app-name```.
  - Click Create Group.

  2. Create a policy
  - Click Policies in the nav bar on the left of the screen.
  - From here, click Create Policy.
  - On the create policy page click on the JSON tab and then the actions dropdown menu and select "Import policy".
  - Search for S3 and select the "AmazonS3FullAccess" policy.
  - You will need to navigate back to your relevant S3 bucket and copy your Amazon Resource Name (ARN)
  - Once copied to your clipboard go back to the create policy page and add the arn to the resource key. This allows all S3 actions both on our bucket itself and the files within it. It should look something like this:
  ```
    "Resource": [
        "your-ARN-here",
        "your-ARN-here/*"
    ]
  ```
  - Once you have done this, click next.
  - Now you can give the policy a name and a description for example the name being, your-app-name-policy and a description something like "Access to S3 bucket for your-app-name static files"
  - Then click Create Policy. This will take you back to the policies page where we can see our policy has been created.
  3. Attach the policy to the user group
  - You will now need to go to User Groups on the left side of the page, click on your relevant group, and then click on the permissions tab.
  - From here you will need to click on the add permissions dropdown and click on attach policies.
  - Search for the policy you have just created select it and click Add permissions at the bottom of the page.
  4. Create a new user
  - Now go on to the Users page on the left of the screen then click Create user.
  - Create a user named your-app-name-staticfiles-user and click next.
  - You will now want to add this user to the relevant group and then click next. You will not need to add anything else so just click through to the end and click Create User.
  5. Download the .csv file
  - Go to IAM and select 'Users'
  - Select the user for whom you wish to create a CSV file.
  - Select the 'Security Credentials' tab
  - Scroll to 'Access Keys' and click 'Create access key'
  - Select 'Application running outside AWS', and click next
  - On the next screen, you can leave the 'Description tag value' blank. Click 'Create Access Key'
  - Click the 'Download .csv file' button. This will contain the user's access key and secret access key. We will use these to authenticate them through our Django app. It is very important that you download and save this as we will not be able to access this again.

### 7. Connecting Django to S3
1. Install packages boto3 and django storages with the following terminal commands:
```
  pip3 install boto3
  pip3 install django-storages
```
2. Freeze your requirements with the following terminal command:
```
  pip3 freeze > requirements.txt
```
3. Add ```'storages',``` to the bottom of your installed apps in your settings.py file
4. To connect Django to S3 we need to add some other settings in settings.py
- Add the following settings just under you MEDIA_URL and MEDIA_ROOT settings.
```
  if 'USE_AWS' in os.environ:
    AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
    AWS_S3_REGION_NAME = 'eu-west-2' # Enter your region name here
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
```
5. With that addeed, you will need to go to heroku and add your AWS keys to the config variables under settings in your relevant app.
6. Add your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY as config variables. Their values can be found in the .csv file you downloaded earlier. You will also need to add the USE_AWS key which we will set to True.
7. While were here we can remove the DISABLE_COLLECTSTATIC variable. As Django should now collectstatic files and automatically upload them to S3.
8. Back in your settings.py file we need to tell Django where our static files will be coming from in production. Which we can do with the following line (In the if statement in step 4.):
```
  AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
```
9. We now need to tell Django that in production we want to use S3 to store our static files whenever someone runs collectstatic and that we want any uploaded product images to go there also. To do this follow these steps:
- create a new file in the root directory named ```custom_storages.py```
- In this file at the top import django settings and s3boto3 storage class from django storages.
```
  from django.conf import settings
  from storages.backends.s3boto3 import S3Boto3Storage
```
- Then create the following classes:
```
  class StaticStorage(S3Boto3Storage):
      location = settings.STATICFILES_LOCATION


  class MediaStorage(S3Boto3Storage):
      location = settings.MEDIAFILES_LOCATION
```
10. Back in our settings.py file add the following settings:
```
    # Static and media files
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATICFILES_LOCATION = 'static'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    MEDIAFILES_LOCATION = 'media'

    # Override static and media URLs in production
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
```
11. Now we can add, commit and push our changes to GitHub. This will make Heroku run ```python3 manage.py collectstatic``` during the build process and upload our static files to S3.
12. We can now go to our Heroku app page and view the build log and the click on Open app to view our app to see if our staticfiles have now been uploaded. We can also look at our S3 bucket page and we should see a static folder containing all of our static files.

### 8. Media Files
1. (Optional) We can add an optional setting to cache our static files. This will improve performance for our users. If you would like to add this functionality add the following code to the top of your ```if 'USE_AWS' in os.environ:``` statement.
```
  # Cache Control
  AWS_S3_OBJECT_PARAMETERS = {
      'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
      'CacheControl': 'max-age=94608000',
  }
```
2. We can now add and commit that then push to GitHub
3. Now go to S3 and under your app create a new folder called media and click create folder.
4. Inside of this folder click upload, add files and then select all the product images.

