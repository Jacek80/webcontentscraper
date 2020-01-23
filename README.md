# webcontentscraper

## Application for scraping images and text content for given URL address

Installation
------------------------------
- Clone the repo
- Run `docker-compose up -d`
- Register user in the app
- Login and get to the `/scraper/api/`

Usage/Allowed methods
------------------------------

- CRUD
- url endpoints to download images/text - on details page `/scraper/api/1/`
- can work in asynchronous mode - check settings flag `RUN_IN_ASYNC_MODE`
- can work with external storage - `MEDIA_ROOT` setting to be adjusted
