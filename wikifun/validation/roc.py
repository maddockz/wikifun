#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Compute the ROC curve for different prediction methods
"""
__author__ = 'maddockz'

import sklearn.metrics as metrics
import numpy as np
import matplotlib.pyplot as plt
import pkg_resources as pkgr

_plots_path = pkgr.resource_filename('wikifun', '../plots/')

def plot_all(pred_tuple, filename='roc.png'):
    """
    Plot ROC curves for all pred_tuples (maximum 5).
    :param pred_tuple: list [tuple] of form (label, y, proba)
    :return:
    """
    plt.clf()
    colors = ["red","blue","green","orange","yellow"]
    for (label, y, proba), color in zip(pred_tuple, colors):
        true_pos, false_pos, thresh = metrics.roc_curve(y, proba)
        plt.plot(false_pos, true_pos, label=label, linewidth=2,
                 color=color)
    plt.plot([0,1],[0,1], linestyle="dashed", color="grey", label="random")
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver Operating Characteristic")
    plt.legend(loc="lower right")

    plt.show()
    plt.savefig(_plots_path + filename)

