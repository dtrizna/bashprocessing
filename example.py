from bashprocessing import Parser

with open(r'all.cm', encoding='utf-8') as f:
    data = f.readlines()

p = Parser(debug=True, verbose=True)

counted = p.parse(data)

print(len(counted))
print(counted.most_common(10))
#import pdb; pdb.set_trace()