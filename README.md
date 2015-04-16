# README #

### What is this repository for? ###

* The ultimate goal is to practice Naive Bayes classification on Wikipedia 
  articles by attempting to automatically determine from the text of the 
  article whether the topic the article falls in a 'History' category.
  
  In the first stage, we extract/transform/load a Wikipedia archive dump into a
  MySQL database.  (Since the dump is large, this is time-consuming.)  
  
  Then a naive bayes model is fit to the data.  We later shall compare this 
  to a 

* Version 1.0

### How do I get set up? ###

* Summary of set up

    1) Download a dump of the Wikipedia archive and save it in the
       ./data directory as a .xml.bz2 file.
       (cf. http://en.wikipedia.org/wiki/Wikipedia:Database_download)
 
    2) Set up a MySQL server to host the upload of the parsed archive.

    3) Modify ./config.py, adding the .xml.bz2 filename, and the
       MySQL database configurations.
    
    4) Replacing <max> with an integer number of articles to import into 
       MySQL, execute  
         >$ python -m wikifun.etl <max>
       to begin creating the database.
    
    5) 
       

* Dependencies: numpy, nose, bz2, peewee

* Database configuration in ./config.py
    * Must be MySQL

* How to run tests:  $ nosetests -v

* Deployment instructions

### Contribution guidelines ###

* Writing tests: Do it for each new feature using nose
* Code review
* Other guidelines

### Who do I talk to? ###

* Me (Zach)