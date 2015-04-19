# README #

### What is this repository for? ###

* The ultimate goal is to practice Naive Bayes classification on Wikipedia 
  articles by attempting to automatically determine from the text of the 
  article whether the topic the article is in a category containing the word 
  'history'.
  
  In the first stage, we extract/transform/load a Wikipedia archive dump into a
  MySQL database.  (Since the dump is large, this is time-consuming.)  
  
  Then a naive bayes model is fit to the data.  We later shall compare this 
  to a more sophisticated hierarchical model.

* Version 1.0

### How do I get set up? ###

* Summary of set up

    1) Download a dump of the Wikipedia archive and save it in the
       ./data directory as a .xml.bz2 file.
       (cf. http://en.wikipedia.org/wiki/Wikipedia:Database_download)
 
    2) Set up a MySQL server to host the upload of the parsed archive.  Make 
       sure to give the user in ./config.py full permissions to the database.

    3) Modify ./config.py, adding the .xml.bz2 filename, and the
       MySQL database configurations.
    
    4) Replacing <max> with an integer number of articles to import into 
       MySQL, execute  
         >$ python -m wikifun.etl <max>
       to create the database and compute the features (word frequencies) of 
       training and testing datasets (10,000 samples each).  
       
       (On my device, this takes roughly 15 hours to extract all articles 
       into MySQL database.  Takes an additional 4 hours to compute 
       all word frequencies on the 20,000 articles.)  
    
    5) Finally, to fit the naive bayes model and see a ROC curve, import the 
       module wikifun.validation.idiots_bayes_plots and call the roc_curve() 
       function. 
       

* Dependencies: numpy, nose, bz2, peewee, MySQLdb

* Database configuration in ./config.py
    * Uses MySQL database

* How to run tests:  $ nosetests -v

* Deployment instructions

### Contribution guidelines ###

* Writing tests: Do it for each new feature using nosetests


### Who do I talk to? ###

* Me (Zach)