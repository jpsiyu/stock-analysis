import matplotlib.pyplot as plt
import matplotlib.font_manager as mfm
import matplotlib.ticker as plticker
import numpy as np
import os

def setFont():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fontPath= os.path.join(dir_path, '../font/Songti.ttc') 
    font = mfm.FontProperties(fname=fontPath)
    return font
font = setFont()

def style(title, xlabel, ylabel, yGrid=False):
    fontSetting = {'fontproperties': font, 'size': 12}
    plt.title(title, **fontSetting)
    plt.xlabel(xlabel , **fontSetting)
    plt.ylabel(ylabel, **fontSetting)

    axes = plt.gca()
    axes.yaxis.grid(yGrid)
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    plt.xticks(rotation=45)

    plt.text(0.05, 1,'(百万)',
        horizontalalignment='center',
        verticalalignment='center',
        transform = axes.transAxes,
        **fontSetting)


def line(x, y, title='', xlabel='', ylabel=''):
    plt.figure(figsize=(8,4))
    style(title, xlabel, ylabel, yGrid=True)

    plt.plot(x, y)
    plt.plot(x, y, 'bo')
    plt.show()


def bar(x, y, title='', xlabel='', ylabel=''):
    plt.figure(figsize=(8,4))
    style(title, xlabel, ylabel) 

    y = y.astype(float)
    yStep = round((y.max() - y.min())/5, 1)
    yMin = round(y.min())
    yMax = round(y.max() + yStep, 1)
    yt = np.arange(yMin, yMax, yStep)
    plt.yticks(yt)

    plt.bar(x, y, 0.3)
    plt.show()