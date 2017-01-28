# Unbabel Backend Challenge

#### The Task: Build a multilingual Hackernews.

Create a multilingual clone of the Hackernews website, showing just the top 10 most voted news and their comments. 
This website must be kept updated with the original hackernews website (every 10 minutes).

Translations must be done using the Unbabel API in sandbox mode. (Ask whoever has been in contact with you about the credentials)

Build a basic view to check the status of all translations.


#### Requirements 
* **[Done]** Use a queue system of your liking: 
    * Going with Celery (with RabbitMQ as broker)
    * Had to learn this from scratch, great learning experiment.
* **[Done]** MongoDB
    * Had to learn this from scratch, great learning experiment.
* **[Done]** Create a scalable application. 
* **[Done]** Only use Unbabel's Translation API on sandbox mode
* **[Done]** Have the news titles translated to 2 languages
* **[Not Completed]** Have unit tests
    * Ran out of time :)
* **[Done]** We dont really care much about CSS but make it so that any developer can understand what you did
    * Front is just a simple page comprised of Html/Css ripped from the HackerNews website itself :)
* **[Done]** Page load time shouldn't exceed 2 secs

#### Resources
* Unbabel's API: http://developers.unbabel.com/
* Hackernews API: https://github.com/HackerNews/API

#### Status

0. Set up basic server infrastructure
1. Study about Celery and try to use it in a simple way
2. Study about Mongo, its concepts and how to use it
3. Simple solution analysis and documentation
    * Component Diagram / Solution Sketch (doc/01__\*.\* files)
4. Kickstart the solution's code structure.
    * Module hierarchy for the solution:, with shared portions.
        * FlaskApp Runner and View Stubs
        * CeleryApp Runner and Task Stubs
        * Shared Portions
            * App Bootstrap Code
            * Database Connector and "Engine" Class (Keep all bare database logic inside one simple structure that is going to be used in all the controllers in both parts of the solution)
            * Simple Controller Base Classes
            * Simple Config System
            * Simple Logging System
            * Utilities, Base "Loggable" Classes, etc
    * Scratchpad (test.py)
5. Implemented Hacker News Item Fetcher with reentrant locks for long-running tasks and support for automatically updating modified entries/comments on Hacker News.
    * HackerNews Controller
        * Responsible for everything related to fetching and updating item data from HN.
    * MongoFunLockController and MongoFunLock
        * Controller+Decorator solution that adds MongoDB-backed task locking capabilities to Celery-based processes. 
            * *I have decided to implement this to cover all bases, should the periodic Hacker News item updater task take more than the alotted 10 minutes specified as the update window... if time runs out, the scheduler will cleanly exit and won't trash the queue system or create a loop :-)*
6. Implemented Item Translation using Unbabel API
    * Implemented UnbabelTranslationController
    * Implemented UnbabelSimpleApi Class
        * *NOTE: Unbabel-py Python Module is not working with the Unbabel API. I had to implement my own simple component based on Unbabel's sources*
    * Implemented Celery Scheduled Tasks for monitoring untranslated items.   
7. Flask Web View of the downloaded data.
    * MainView (index)
    * StoryComments
8. Website deployed and running at **http://unbabelchallenge.angrybits.org:5000/**
    * Since this is just a challenge/toy project, I did not bother to deploy to nginx+uWSGI. We are using Flask's built-in server.
    * Going to leave this running for a few days so you can assess. Also if you need SSH access to the live running app, just ask.
9. Task completed. 

#### Set up

- Set up a Linux Box (tested on Ubuntu 16.04 x64)
- Clone this repo.
- Have Python3.5 and "virtualenv" tools installed.
- Read **docs/00__infrastructure_bootstrap.txt** on tips on how to set up the project's system dependencies (mongodb, rabbitmq). Both are used with their default configs, serving unauthenticated connections on localhost only. 
- From the project root, issue the following shell command to create the virtual environment and install all the project's direct dependencies via pip:
```$ . doc/virtualenv/create_virtualenv.sh```
    
#### Running it 

(Celery counterpart)

- Make sure rabbitmq and mongodb are running.
- Go to project root:
    * Activate the virtual env with```$ . venv/bin/activate ``` 
    * Run: ```$ ./runcelery.sh```
- You should be able to see celery running with some tasks registered, and after 10 minutes , it'll start fetching and updating our local MongoDB with Hacker News Items. 

(Flask counterpart)

- Make sure rabbitmq and mongodb are running.
- Go to project root:
    * Activate the virtual env with```$ . venv/bin/activate ``` 
    * Run: ```$ ./runflask.sh```
- Access the webpage at (URL) to view the website. 


    


