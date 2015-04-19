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
* An uninformative prior C ~ Bernoulli(0.5)

Simplified Idiot's assumptions: (implemented here)
* L and C are independent (Likely an incredibly idiotic assumption!)
* L and p are independent (Perhaps less unreasonable assumption)
* Replace p with point estimates p_hat, using (smooth) instead of (ML):
  * (ML) p_hat = N_C/N_tot
    where N's are word counts in category or total
  * (smooth) p_hat = (N_C + alpha)/ (N + alpha * n)
    where alpha is smoothing param

Our classifier is then determined via a MAP (maximum a posteriori) estimate.
One may use either the observed category frequency as point estimate for prior
distributions of C:
  C ~ Bernoulli( # C-articles / # total articles ).
Or one may choose not, and keep our uninformative prior C ~ Bernoulli(0.5).

Note: The log of the (numerator of) the posterior density is linear in F,
and therefore the decision boundary will be linear.
"""

from sklearn.svm.libsvm import fit

__author__ = 'maddockz'

import random
from sklearn import naive_bayes as nb
import numpy as np
from scipy import sparse


import wikifun.etl.data_models as dm
import wikifun.etl.sample as sample


def make_X(articles):
    """
    Creates sparse training matrix X from a list of articles
    :param articles: list of [dm.Article]
    :return: sparse.coo.coo_matrix
    """
    n_words = np.sum(1 for _ in dm.Word.select() )
    X = sparse.lil_matrix((0, n_words), dtype=int)
    for article in articles:
        print u'Extracting article: {0}'.format(article.title)
        row = np.ndarray((1,n_words), dtype=int)
        row.fill(0)
        # Iterate over all words in article
        word_freqs = dm.WordFreq.select().where(dm.WordFreq.article == article)
        for word_freq in word_freqs:
            word_index = word_freq.word.id - 1
            row[0,word_index] = word_freq.freq
        if X.shape[0] == 0:
            X = sparse.lil_matrix(row)
        else:
            X = sparse.vstack([X, sparse.lil_matrix(row)])
    return X

def make_y(articles):
    """
    Creates training target matrix y from a list of articles.
    :param articles:
    :return: np.ndarray
    """
    n_arts = len(articles)
    y = np.ndarray((n_arts,), dtype=bool)
    y.fill(False)
    for i, article in enumerate(articles):
        if article.is_history:
            y[i] = True
    return y

def fit_model(X, y):
    nbm = nb.MultinomialNB(alpha=1.0, fit_prior=True)
    print 'Fitting model on {0} articles...'.format(len(y))
    nbm.fit(X,y)
    print 'Model fit!'
    return nbm

def main():
    """
    Returns naive bayes model fit on cached (pickled) training data
    :return: nb.MultinomialNB
    """
    train_ids, test_ids = sample.get_cached_ids()
    train = sample.get_articles(train_ids)
    X, y = make_X(train), make_y(train)
    return fit_model(X, y)


if __name__ == '__main__':
    main()