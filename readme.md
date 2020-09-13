# The GIS Jobs Map

Source code for [The GIS Jobs Map](http://gisjobsmap.com)

## About
This is a side project I hacked together over the years, it is undoubtedly a work in progress and in need of improvement. 
There are many features that were half-built and never completed (additional map layers and a user authentication system for instance), 
so dont be alarmed if something doesnt make sense. I am unable to continue building features due to lack of time, but feel free to fork it and make it your own. 
If you see an issue or like to contribute, PRs are welcome.  

 
## Quick Start
1. Review the `.env` files in the docker directory
2. `docker-compose build`
3. `docker-compose up -d`
4. `docker-compose exec backend python manage.py init_geo` # populates geonames and worldborders tables
5. `docker-compose exec backend python manage.py init_data` # loads tags, categories and user accounts

### Production
all the above commands should be run with the `-f docker-compose.prod.yml` argument. Here are a couple other scripts that are useful: 


Initialize Lets Encrypt:

`scripts/init-letsencrypt.sh`

Rebuild and deploy subsequent code changes:

`sudo sh scripts/rebuild-prod.sh`

## Services
### scraper
Scrapes GIS jobs from the indeed api. To get around the Request Limit restriction, you need to rotate proxies. 
I use a paid proxy service through [Private Internet Access](https://www.privateinternetaccess.com/) which works well. 
It can probably be changed to rotate through free proxies at the expense of speed/reliability. Either way Indeed probably 
doesnt like this and its most likely against their TOS, so be aware of that. 

The other requirement is to obtain an API Key with an [Indeed publisher](https://www.indeed.com/publisher) account.

### backend
The web api built with Flask. There are several endpoints of varying degrees of completion and implementation. Browse 
the tests and codebase to see whats working and not. 

Built with:
 - Flask
 - SQLAlchemy / GeoAlchemy
 
The admin UI can be accessed at the /admin endpoint.

### client
Frontend application and web server

Built with:
 - reactjs
 - redux
 - leaflet
 - ant design

served with nginx (production)

###  jobs-db
contains the main application data.

### geonames-db
contains (mostly) geonames data used for geocoding and other spatial queries.

## database migrations
initialize:

 `docker-compose exec backend python manage.py db init`
 
 Make migrations:
 
 `docker-compose exec backend python manage.py db migrate`
 
 Upgrade migrations:
 
 `docker-compose exec backend python manage.py db upgrade`

## Tests
#### backend
 `docker-compose exec backend python manage.py test`
 
### client
TODO

### scraper
`docker-compose exec scraper python -m unittest`

# Contribute
If you are interested in contributing, PR's are welcome. Ideally any significant changes should be accompanied with tests. 
