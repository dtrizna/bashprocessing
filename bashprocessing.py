import numpy as np
import bashlex
import re
import nltk
from collections import Counter, defaultdict

class Parser():

    def __init__(self, debug=False, verbose=False):
        self.ERR = 0
        self.debug = debug
        self.verbose = verbose

        self.data = None
        self.global_counter = None
        self.corpus = None

        self.tokenized_node = None


    def bashlex_wrapper(self, command):
        try:
            nodes = bashlex.parse(command)
            return nodes
        # bashlex fails to parse some syntax combinations
        # in that case split command by <space>, <comma>, <curly_brackets>
        # and add values in between directly to counter as keys
        except (bashlex.errors.ParsingError, NotImplementedError, TypeError):
            self.ERR += 1
            rude_parse = []
            for element in re.split(r" |,|{|}",command):
                rude_parse.append(element)
            return rude_parse


    def update_objects(self, counters, tokens):
        self.global_counter += counters
        self.tokenized_node.extend(tokens)

    # self-calling iterative function
    def iterate_bashlex(self, bashlex_object):
        local_cntr = Counter()
        local_tokens = []

        if isinstance(bashlex_object, list):
            for element in bashlex_object:
                self.update_objects(*self.iterate_bashlex(element))
        
        elif isinstance(bashlex_object, bashlex.ast.node):
            object_methods = [x for x in dir(bashlex_object) if '__' not in x]
        
            # handling different bashlex object types into elements of Counter()
            if 'command' in object_methods:
                self.update_objects(*self.iterate_bashlex(bashlex_object.command))
            
            elif 'list' in object_methods:
                for element in bashlex_object.list:
                    self.update_objects(*self.iterate_bashlex(element))
            elif 'parts' in object_methods:        
                # if parts have parts within - go deeper 
                # (Leo from Inception looking at you)
                if bashlex_object.parts:
                    for part in bashlex_object.parts:
                        self.update_objects(*self.iterate_bashlex(part))
                else:
                    local_cntr, local_tokens = self.parse_word(bashlex_object)
            elif 'word' in object_methods:
                local_cntr, local_tokens = self.parse_word(bashlex_object)
            
            # Working on default specific types
            elif 'value' in object_methods:
                self.global_counter[bashlex_object.value] += 1
                self.tokenized_node.append(bashlex_object.value)
            elif "pipe" in object_methods:
                self.global_counter[bashlex_object.pipe] += 1
                self.tokenized_node.append(bashlex_object.pipe)
            elif "op" in object_methods:
                self.global_counter[bashlex_object.op] += 1
                self.tokenized_node.append(bashlex_object.op)
            elif "type" in object_methods:
                self.global_counter[bashlex_object.type] += 1
                self.tokenized_node.append(bashlex_object.type)
            else:
                if self.debug:
                    print("{DEBUG} Weird case - not parsed correctly:", bashlex_object)
                    import pdb; pdb.set_trace()
        
        return local_cntr, local_tokens


    def parse_word(self, bashlex_object):
        local_cntr = Counter()
        local_tokens = []
        size = 1
        # Trying to parse input object again
        # helps if previous parse iteration didn't handled
        # some fragments of command (e.g. $(), ``, embedded ones)
        word = re.sub(r"[<>#{}]", "", bashlex_object.word).strip()
        if len(bashlex_object.word) > 20:
            p = self.bashlex_wrapper(word)
            if isinstance(p[0], bashlex.ast.node):
                try:
                    size = len(p[0].parts)
                except AttributeError:
                    size = len(p[0].list)
        # if size > 1 then parsing found something new
        if size > 1:
            for node in p:
                self.update_objects(*self.iterate_bashlex(node))
        
        # if no new elements - improve bashlex parsing of flags w/ '='
        elif '=' in bashlex_object.word and \
        '==' not in bashlex_object.word:
            l = bashlex_object.word.split('=')
            # special case
            if 'chmod' in bashlex_object.word.lower():
                local_cntr[l[0]] += 1
                local_cntr['='.join(l[1:])] += 1
                local_tokens.extend([l[0], '='.join(l[1:])])
            # standard 'flag=value' case
            elif len(l) == 2:
                local_cntr[l[0]] += 1
                local_cntr[l[1]] += 1
                local_tokens.extend([l[0], l[1]])
            # weird combination - add as is
            else:
                local_cntr[bashlex_object.word] += 1
                local_tokens.append(bashlex_object.word)
 
        # bashlex parsing correct
        else:
            local_cntr[bashlex_object.word] += 1
            local_tokens.append(bashlex_object.word)

        return local_cntr, local_tokens

    
    def parse(self, data, ret='counter'):
        self.data = data
        self.global_counter = Counter()
        self.corpus = []
        
        l = len(data)
        for i,command in enumerate(data):
            self.tokenized_command = []
            
            if self.verbose:
                print(f"[!] Parsing in process.. {i}\{l}", end="\r")
            
            # bashlex wrapper returns list
            nodes = self.bashlex_wrapper(command)
            
            # if it consists of strings - the parsing failed and rude splitting is performed
            # add splitted command to corpus as is
            if isinstance(nodes[0], str):
                #if self.debug:
                    #print(f"failed parsing case: {nodes}")
                    #import pdb; pdb.set_trace()
                self.tokenized_command.extend(nodes)
                self.global_counter += Counter(nodes)
            
            # if it consists of bashlex nodes - parsing suceeded
            elif isinstance(nodes[0], bashlex.ast.node):
                for node in nodes:
                    self.tokenized_node = []
                    self.update_objects(*self.iterate_bashlex(node))
                    self.tokenized_command.extend(self.tokenized_node)
            
            # weird ..
            else:
                print("[-] Unexpected return type from bashlex_wrapper!")
                if self.debug:
                    import pdb; pdb.set_trace()
                raise TypeError

            self.corpus.append(self.tokenized_command)
        
        return self.global_counter, self.corpus
    

    def encode(self, cntr, mode='tf-idf', data=None, sklearn=False):
        if not self.data and not data:
            print("[!] Please specify your data or parse it beforehand!")
            return None
        else:
            data = data if data else self.data
        
        if mode == 'tf-idf':
            # TODO
            # Need to create corpus of data: 
            # list of documents, where documents is list of tokens
            """
            word_idf_values = defaultdict(float)
            l = len(cntr.keys())
            for i,token in enumerate(list(cntr)):
            
                if self.verbose:
                    print(f"[!] TF-IDF encoding: {i}\{l}", end="\r")
                cmd_containing_word = 0
                for i, cmd in enumerate(data):
                    print(self.parse([cmd]))
                    #if token in self.parse([cmd]):
                    #    cmd_containing_word += 1
                #word_idf_values[token] = np.log(len(data)/(1 + cmd_containing_word))""" 