import matplotlib.pyplot as plt
import matplotlib.font_manager as mfm
import matplotlib.ticker as plticker
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
    plt.xticks(rotation=45)

    axes = plt.gca()
    axes.yaxis.grid(yGrid)
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)

    loc = plticker.MultipleLocator(base=1.0)
    axes.xaxis.set_major_locator(loc)


def line(x, y, title='', xlabel='', ylabel=''):
    plt.figure(figsize=(8,4))
    style(title, xlabel, ylabel, yGrid=True)

    plt.plot(x, y)
    plt.plot(x, y, 'bo')
    plt.show()


def bar(x, y, title='', xlabel='', ylabel=''):
    plt.figure(figsize=(8,4))
    style(title, xlabel, ylabel)

    plt.bar(x, y, 0.3)
    plt.show()