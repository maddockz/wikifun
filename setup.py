try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
          'description': 'Classification of Wikipedia articles via Naive Bayes algorithm',
          'author': 'Zachary Maddock and Thomas Nyberg',
          'url': 'https://github.com/maddockz/wikifun/',
          'author_email': 'maddockz@gmail.com',
          'version': '0.1',
          'install_requires': ['nose'],
          'packages': ['wikifun'],
          'scripts': [],
          'name': 'wikifun'} 

setup(**config)