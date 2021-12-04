
# Combining Dash and Flask
[Turkish PDF Link where each code is explained in detail](https://drive.google.com/file/d/1jy65z91ytZShthRkem8gx2qZvGSUQcf4/view?usp=sharing)


## Technologies Used (Requirements)
- Flask
- Dash
- Plotly
- Pandas
- You can check the **requirements.txt** file for all packages.


## Project Structure
### Structure
- Project stands up from **wsgi.py** file
- Thanks to the **fetch_all.py** file in the root directory (cronjob attached to the system runs this file) fetch_data.py under all dash application directories is run.
    - In this way, updated data is taken from the data warehouse every night at 00:00 and our python project is restarted at 03:00 and the current data is included in the dashboards.
- **__init.py__** creates our main FLASK application
- **app.py** contains components of our main FLASK application (blueprints, routes, handlers etc)
- The **myconfig.py** file in the main directory holds the settings of the Flask application (static path, development mode etc.).
- All functions, modules, packages etc. related to the project are collected under the **flaskapp** folder.
- We can access DASH applications under the **flaskapp/dashboard** folder.
- **flaskapp/dashboard/utilites/database_config.py** file contains pymssql config information to connect to the warehouse
- There are functions to make our work easier under the **flaskapp/dashboard/utilities** folder, if any, components etc.
- Under the **flaskapp/static** folder, static files (bootstrap, jquery etc.) of the FLASK application are kept.
- Under the **flaskapp/templates** folder, the template files (jinja2, html etc.) returned by the routes belonging to the FLASK application are kept.
- Under the **flaskapp/dashboard/apps** folder, there are folders **for each dash** application.
    -  Under **app.py** DASH app stands up
        - **BASE_URL** constants give us the link to be used as an iframe. -> EX: www.xyz.com/BASE_URL
        - **APP_NAME** constants determine the name of the DASH application when sending it to FLASK (navbar, context processors, etc.)
    - The data to be sent to the DASH application under **data.py** is prepared / pulled
    - Under **fetch_data.py** data is extracted from the data warehouse, processed and exported as csv to the directory where it is located.
    - **\*.xlsx/\*.csv** files are added under the same directory if the data set is not extracted from SQL

### Directory Structure
```
.
├── admin
├── dashboard
│   ├── apps
│   │   └── developer
│   │       └── screens
│   │           ├── basic_components
│   │           └── bizim
│   └── utilities
│       ├── components
│       └── data
├── models
│   └── utilities
├── static
│   ├── Toast
│   ├── css
│   ├── img
│   ├── js
│   └── node_modules
└── templates
    ├── admin
    ├── dashboards
    └── utilities
```

### Working logic

***You can check the `developer` dash app folder for inspecting the system.**

We create a FLASK application under **__init__.py**.

Under **app.py** we define components of our core FLASK application.

Then, while initializing each DASH application we create, we set the server parameter as the FLASK application we created. 

In this way, all our DASH applications and our FLASK application run on the same server.

While the FLASK application stands up, the DASH applications we mount on it also stand up. Thanks to the iframe urls defined in urls.py, we can use our DASH applications in our FLASK application.

Under /dashboard/urls.py, we add the CONFIG constants for each app. In this way, we can perform our route operations through these constants.

We call our FLASK application from **wsgi.py** file (naturally all DASHs binded to it) and serve on the server.

Under the **fetch_all.py** file, fetch_data modules belonging to all dash applications are called and fetch_data functions are executed. In this style, the cronjob will run this file the night before and it will take a long time. After this process is completed, it will restart our flask application. In this way, the new data captured will be included in the project.

### An Example CONFIG Constant
```
CONFIG = {
    'BASE_URL': '/pure/dashboard-name/', # iframe address (url)
    'APP_URL': 'dashboard-name', # The key ('/' should not be used), which is listed on the navbar and enables us to perform the route operation, at the same time we can do the authorization process thanks to this constant.
    'APP_NAME': 'Dashboard Name', # name to appear in template (Flask)
}
```
### Component Builder
The Component Builder developed based on [Bulma CSS](https://bulma.io/). You can follow this path for inspecting the components: `flaskapp/dashboard/utilities/components/builder.py`