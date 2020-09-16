Pre-processing depends on `bashlex` (https://github.com/idank/bashlex) library.  
  
Dataset (i.e. `all.cm`) is based on `nl2bash` paper (https://arxiv.org/abs/1802.08979; https://github.com/TellinaTool/nl2bash).  

Plan is to:

1. Implement POS tagger

2. Encoding: TF-IDF, LabelEncoder, OneHotEncoder

3. Prepare for usage as an external Class for community usage, e.g.:
```
from bashprocessing import Parser, PosTager

p = Parser(depth=5)
parsed_data = p.start(raw_commands)

pos = PosTagger()
tagged_data = pos.tag(parsed_data)
```