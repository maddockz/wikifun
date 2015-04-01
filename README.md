# README #

I haven't written anything yet.

### What is this repository for? ###

* The ultimate goal is to practice Naive Bayes classification on Wikipedia 
  articles by attempting to classify articles as 'History' or 'Sports'.  
  
  In the first stage, we clean a dump of a Wikipedia archive and store it in 
  a MySQL database.  Perhaps this will more useful to other users than the
  analysis that follows. 

* Version 1.0

### How do I get set up? ###

* Summary of set up

    1) Download a dump of the Wikipedia archive and save it in the
       ./data directory as .xml.bz2 file.
       (cf. http://en.wikipedia.org/wiki/Wikipedia:Database_download)
 
    2) Set up a MySQL server to host the upload of the parsed archive.

    3) Modify the configuration file ./config.py
    

* Dependencies: numpy, nose, bz2

* Database configuration in ./config.py
    * Must be MySQL

* How to run tests:  $ nosetests -v

* Deployment instructions

### Contribution guidelines ###

* Writing tests: Do it!
* Code review
* Other guidelines

### Who do I talk to? ###

* Me (Zach)