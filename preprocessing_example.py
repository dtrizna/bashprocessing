from bashprocessing import Parser

with open(r'data/bashlex.cm', encoding='utf-8') as f:
    data = f.readlines()

p = Parser(debug=True, verbose=True)

counted, corpus = p.parse(data[0:100])

print("\n", "Total unique elements found: ", len(counted))
print(counted.most_common(5))

"""
% python3 example.py
[!] Parsing in process.. 12606\12607
Total unique elements found: 10372
[('find', 7846), ('|', 6487), ('.', 3775), ('-name', 3616), ('-type', 3403)]
"""

# ENCODING EXAMPLES

labels = p.encode(mode="labels")
"""
(Pdb) labels[0]
array([91,  9, 44, 44, 99, 85, 16, 44, 99, 85, 16, 44])
(Pdb) corpus[0]
['top', '-b', '-d2', '-s1', '|', 'sed', '-e', '1,/USERNAME/d', '|', 'sed', '-e', '1,/^$/d']
(Pdb) len(labels)
1744
(Pdb) len(corpus)
1744
"""

onehot = p.encode(mode="onehot")
"""
(Pdb) dict(counted.most_common(100)).keys()
dict_keys(['|', 'top', ';', 'chmod', '1', '-n', '-b', 'grep', 'find', 'sed', '-p', ...]
(Pdb) corpus[0]
['top', '-b', '-d2', '-s1', '|', 'sed', '-e', '1,/USERNAME/d', '|', 'sed', '-e', '1,/^$/d']
(Pdb) onehot[0]
array([1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
"""

# TF-IDF: NOT YET IMPLEMENTED
tfidf = p.encode(mode="tf-idf")
import pdb; pdb.set_trace()
"""
(Pdb) pprint(tfidf)
    ...
    '~music': 6.214608098422191,
    '–exec': 6.214608098422191,
    '–iname': 6.214608098422191,
    '–l': 6.214608098422191,
    '–p': 6.214608098422191,
    '–print': 6.214608098422191,
    '“HIGHMEM”': 6.214608098422191})
"""