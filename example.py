from process_w_corpus import Parser

with open(r'all.cm', encoding='utf-8') as f:
    data = f.readlines()

p = Parser(debug=True, verbose=True)

counted, corpus = p.parse(data[0:1000])

print("\n", "Total unique elements found: ", len(counted))
print(counted.most_common(5))
"""
% python3 example.py
[!] Parsing in process.. 12606\12607
Total unique elements found: 10372
[('find', 7846), ('|', 6487), ('.', 3775), ('-name', 3616), ('-type', 3403)]
"""

#tfidf = p.encode(counted)
print()
import pdb; pdb.set_trace()