Pre-processing depends on `bashlex` (https://github.com/idank/bashlex) library.  
  
Dataset (i.e. `all.cm`) is based on `nl2bash` paper (https://arxiv.org/abs/1802.08979; https://github.com/TellinaTool/nl2bash).  

Example usage:
```
from bashprocessing import Parser

with open("all.cm") as file:
    data = file.readlines()

p = Parser()
data_counter, data_corpus = p.parse(data)
print(data_counter.most_common(5))

[Out]:
    [('find', 7846),
    ('|', 6487),
    ('.', 3775),
    ('-name', 3616),
    ('-type', 3403)]

encoded_X = p.encode(mode="onehot")
print(encoded_X[0])

[Out]:
    array([1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
```

At this point data is ready to be supplied as input for your ML model:
```
mymodel.fit(X,y)
```

Some ideas of exploratory data analysis can be found under `/eda/`:

![alt text](img/Tux_wordcloud.png =250x100 "WordCloud of most common elements")
![alt text](img/absolute_element_counts.png "Absolute Element Counts")


Next steps:
1. Encoding: TF-IDF
2. ML application example
3. Implement POS tagger
