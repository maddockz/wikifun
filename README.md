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
 
    2) Start a MySQL server to host the wikifun data.  
       Log in as root and execute:
         mysql> GRANT ALL ON wikifun.* TO 'usr_wikifun'@'<hostname>';

    3) Modify ./config.py, adding the .xml.bz2 filename, and the
       MySQL database configurations.  
    
    4) Execute  
         >$ python -m wikifun.etl <max>
       <max> is an optional argument that is an integer limiting number of 
       articles to load into MySQL.  This command creates a MySQL database, 
       loads up to <max> articles.  Then 2 simple random samples of 10k 
       articles are chosen for the test and training sets, and the 
       features (word frequencies) are computed.
       
       (Warning: On my device, it takes roughly 15 hours to load all 
       articles into MySQL database.  Takes an additional 4 hours to compute 
       the word frequency features on the training and test data sets.)   
    
    5) To fit the naive bayes model and generate a ROC curve plot, execute
         >$ python -m wikifun.validate.idiots_bayes_plots

* Dependencies: numpy, nose, bz2, peewee, MySQLdb, sklearn, matplotlib
                

* Database configuration in ./config.py
    * Uses MySQL database

* How to run tests:  $ nosetests -v

* Deployment instructions

### Contribution guidelines ###

* Writing tests: Do it for each new feature using nosetests


### Who do I talk to? ###

* Me (Zach)