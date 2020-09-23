import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import string
import sys

from collections import Counter
from os import path, getcwd

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image

scriptpath = ".."
sys.path.append(path.abspath(scriptpath))
scriptpath = "."
sys.path.append(path.abspath(scriptpath))

from bashprocessing import Parser

try:
    with open('all.cm') as f:
        data = f.readlines()
except FileNotFoundError:
    with open('../all.cm') as f:
        data = f.readlines()

p = Parser(verbose=True)
counter, corpus = p.parse(data)

bash_stopwords = [key for key in counter.keys() if all(key.isdigit() or len(key) < 3 or j in string.punctuation for j in key)]
clean_dict = {key:counter[key] for key in counter.keys() if not all(key.isdigit() or len(key) < 3 or j in string.punctuation for j in key)}


# WORDCLOUD

d = path.dirname(__file__) if "__file__" in locals() else getcwd()

tuxmask = np.array(Image.open(path.join(d, "../img/Tux.png")))#.convert("1")).astype(int)
img_color = ImageColorGenerator(tuxmask)

wc = WordCloud(background_color="white", \
                stopwords=bash_stopwords, \
                max_words=300, \
                contour_width=3, \
                contour_color='steelblue')#,\
                #mask=tuxmask) # Cannot make to work it w/ mask ....

# generate word cloud
wc.generate_from_frequencies(dict(clean_dict))
plt.figure(figsize=(12,8))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()
#plt.savefig('../img/wordcloud.png', bbox_inches='tight')
#plt.close()


# BARCHART

X,Y = zip(*Counter(clean_dict).most_common(12))

sns.set_theme(style="whitegrid")
sns.set(font_scale=1.4)
plt.figure(figsize=(14,6))
bars = sns.barplot(x=list(X), y=list(Y), palette="Blues_d")
#bars.get_figure().savefig("../img/absolute_element_counts.png")
plt.show()
#plt.close()
