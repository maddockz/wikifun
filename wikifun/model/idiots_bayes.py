#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Implements a naive (idiot's) Bayes model (with multinomial likelihood)
under a 'bag-of-words' assumption for (Wikipedia) articles.  This is a
standard algorithm implemented nicely in scikit.learn, but for clarity we
document here the simplifying assumption this classifier makes.

For a given article define the following:

Features:
* F = a vector of word frequencies
* L = the length of the article (# of words)
* C = category of article (either History xor Sports)

Parameters:
* p = a vector of word probabilities.

Full Bayesian assumptions: (will implement in another module)
* The likelihood F|L,p ~ Multi(L,p)
* The entries of the parameter p are iid with Unif(0,1) prior distribution
* An uninformative prior C ~ Bernoulli(1/2)

Simplified Idiot's assumptions: (implemented here)
* L and C are independent (Likely an incredibly idiotic assumption!)
* L and p are independent (Perhaps less unreasonable assumption)
* Replace p with point estimates p_hat.  Ie instead of (ML) we use (smooth):
  * (ML) p_hat = N_C/N_tot
    where N's are word counts in category or total
  * (smooth) p_hat = (N_C + alpha)/ (N + alpha * n)
    where alpha is param

Our classifier is then determined via a MAP (maximum a posteriori) estimate.
One may use either the observed category frequency as point estimate for prior
distributions of C:
  C ~ Bernoulli( # C-articles / # total articles ).
Or one may choose not, and keep our uninformative prior C.

Note: The log of the (numerator) in the posterior density is linear in F,
and therefore the decision boundary will be linear.
"""
from sklearn.svm.libsvm import fit

__author__ = 'maddockz'

import random
from sklearn import naive_bayes as nb
import numpy as np

import peewee as pw

import wikifun.etl.data_models as dm

# Split all articles (with word data computed) into training and test data
query = dm.WordFreq.select(dm.WordFreq.article).distinct()
all_arts = [wf.article for wf in query]

n = len(all_arts)
n_train = (n * 3)/5

train_idx = random.sample(xrange(n), n_train)
train = [all_arts[i] for i in train_idx]
test  = [all_arts[i] for i in xrange(n) if i not in train_idx]

nbm = nb.MultinomialNB(alpha=1.0, fit_prior=True)

def make_X(articles):
    """
    Creates observation matrix X from a list of articles
    :param articles: list of [dm.Article]
    :return: np.array
    """
    words = [word for word in dm.Word.select()]
    print len(words)
    n_words = len(words)
    X = np.ndarray(shape=(0, n_words), dtype=int)
    for article in articles:
        print article.title
        row = np.ndarray(shape=(1,n_words), dtype=int)
        for i in xrange(n_words):
#            q = dm.WordFreq.article == article & dm.WordFreq.word == words[i]
            row[0,i] = 0 #dm.WordFreq.get(q).freq

        X = np.concatenate((X,row), axis=0)
    return X


