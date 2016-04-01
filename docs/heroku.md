# Heroku Deployment

### From scratch

1. Create a new Heroku app. For the purposes of these instructions we'll call it "dce-course-info", but it could really be anything.
1. Install the [heroku-toolbelt](https://toolbelt.heroku.com/).
1. Clone the [dce_course_info](https://github.com/harvard-dce/dce_course_info repo).
1. Run `heroku git:remote -a dce-course-info`
1. Add the required heroku add-ons: 
    * [Heroku Postgres](https://addons.heroku.com/heroku-postgresql) 
    * [RedisToGo](https://elements.heroku.com/addons/redistogo)
1. Set up the remaining environment vars via `heroku config:set ...` (see below)
1. Create a loggly logging drain:
    * `heroku drains:add https://logs-01.loggly.com/bulk/<loggly token>/tag/heroku,dce-course-admin`
1. Run `git push heroku master`. Heroku will detect and build the app.
1. Run `heroku run python manage.py migrate` to initialize the database. 
    * Up to you whether you want to create an admin user. The app doesn't require it.
1. Install the LTI app in the Canvas account settings UI. 
    * Configuration Type: 'By URL'
    * Name: 'Course Info'
    * Consumer Key: value of the **LTI_OAUTH_COURSE_INFO_CONSUMER_KEY** env var
    * Consumer Secret: value of the **LTI_OAUTH_COURSE_INFO_CONSUMER_SECRET** env var
    * Config URL: `https://<app_url>/course_info/tool_config`

### Required env vars

    LTI_OAUTH_COURSE_INFO_CONSUMER_KEY=...
    LTI_OAUTH_COURSE_INFO_CONSUMER_SECRET=...
    DJANGO_SECRET_KEY=...
    PYTHONPATH=fakepath
    REDIS_URL=...

* **LTI_OAUTH_COURSE_INFO_CONSUMER_KEY** and **LTI_OAUTH_COURSE_INFO_CONSUMER_SECRET** are credentials needed during the Canvas LTI app installation. The key should be some simple, identifying string, like "dce-course-admin". For the secret you can probably just use a generated password or a [uuid4](http://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_.28random.29), but if you want to get fancy there's a [secret key generator](http://techblog.leosoto.com/django-secretkey-generation/) that I sometimes use.
* **DJANGO_SECRET_KEY**: see comments above about the *LTI_OAUTH_COURSE_INFO_CONSUMER_SECRET*.
* **PYTHONPATH**: This is a common kludge to deal with [gunicorn weirdness on heroku](https://github.com/heroku/heroku-buildpack-python/wiki/Troubleshooting#no-module-named-appwsgiapp).
* **REDIS_URL**: copy this from the **REDISTOGO_URL** that was inserted into your heroku config when the redis add-on was added.

### Additional env vars

    DATABASE_URL=...

These are all provided by add-ons; do not set them manually.


