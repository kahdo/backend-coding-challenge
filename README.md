# Unbabel Backend Challenge

#### The Task: Build a multilingual Hackernews.

Create a multilingual clone of the Hackernews website, showing just the top 10 most voted news and their comments. 
This website must be kept updated with the original hackernews website (every 10 minutes).

Translations must be done using the Unbabel API in sandbox mode. (Ask whoever has been in contact with you about the credentials)

Build a basic view to check the status of all translations.


#### Requirements 
* Use a queue system of your liking: 
    * Going with Celery (with RabbitMQ as broker)
* MongoDB
* Create a scalable application. 
* Only use Unbabel's Translation API on sandbox mode
* Have the news titles translated to 2 languages
* Have unit tests
* We dont really care much about CSS but make it so that any developer can understand what you did
* Page load time shouldn't exceed 2 secs

#### Resources
* Unbabel's API: http://developers.unbabel.com/
* Hackernews API: https://github.com/HackerNews/API

#### Status

0. Set up basic server infrastructure [OK]
1. Study about Celery and try to use it in a simple way [OK]
2. Study about Mongo, its concepts and how to use it [OK]
3. Simple solution analysis and documentation, kickstart the solution's code structure.
