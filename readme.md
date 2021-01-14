# Flask CMS

This is a revamp of my flask_analytics_file_server to be more of a CMS system and allow easy creation of forum sites, simple html sites, and jinja2 template sites. A database model will be included with this new project instead of it being seperate as before.

The idea behind this project is to be able to have multiple different websites run on one server with varying degrees of complexity BUT be able to track all of them from one place and update them from one place.

This project allows you to host multiple static websites with one flask application and track visits to each site. The analytics part of this project was the first thing I created in python besides the basic textbook projects so it requires some polish...

## Why would someone want to use this project?
* To host multiple static (html, css, js) websites on one server without setting up Apache/Nginx/etc for each one.
* To create your own web hosting service
* To track analytics of your website visits without using a 3rd party like google analytics

## To Do:
* Login page for analytics
* Make the analytics page more graphical?
* More useful analytic views
* Why is epoch time being used??? Why not just use date/time.. Over complicating something simple.....

## Settings
Create files called secrets.py in the main directory.

In the secrets.py file you will need to tell the application your Google API keys and MySQL database information.

In the settings.py file you need to tell the application what websites you will be hosting and if you have your website in a different folder that the domain name. You can also configure the bad url, bad user agents, user agents that are ok but dont track, etc in this file.

By default the application will try to use the domain as the folder name if a folder is not specified. A good use case for this is if you are on your local computer and run the flask application then the domain is 127.0.0.1:5000 but we can not use : in our folder names so our files can not be in a folder with :. Another use case if if you have multiple domains you want to point towards the same folder. For example you have 1967skylark.com and 67skylark.com are you going to make a website for each one or copy/paste teh same files to another folder? Most likely not. You just want to direct them to the same folder. Why would you want two domains that are similar anyways?...................


```
# secrets.py
secrets = {
    "google": {
        "client": "",
        "secret": ""
    },
    "sql": {
        "host": "127.0.0.1",
        "port": 3306,
        "db": "",
        "table": "",
        "username": "",
        "password": ""
    }
}

```

## Adding a new website
Once you have domain dns settings setup and the domain added to the websites variable in the settings.py file all you need to do is add your files to the **./websites/** folder.