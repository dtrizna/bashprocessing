import numpy as np
import bashlex
import re
from collections import Counter

class Parser():

    def __init__(self, debug=False, verbose=False):
        self.ERR = 0
        self.debug = debug
        self.verbose = verbose

    def bashlex_wrapper(self, command, cntr):
        try:
            nodes = bashlex.parse(command)
            return nodes
        # bashlex fails to parse some syntax combinations
        # in that case split command by <space>, <comma>, <curly_brackets>
        # and add values in between directly to counter as keys
        except (bashlex.errors.ParsingError, NotImplementedError, TypeError):
            for element in re.split(r" |,|{|}",command):
                cntr[element.strip()] += 1
            self.ERR += 1
            return None


    # self-calling iterative function
    def iterate_bashlex(self, bashlex_object):
        output_cntr = Counter()
        
        if isinstance(bashlex_object, list):
            for element in bashlex_object:
                output_cntr += self.iterate_bashlex(element)
        
        elif isinstance(bashlex_object, bashlex.ast.node):
            object_methods = [x for x in dir(bashlex_object) if '__' not in x]
            # handling different bashlex object types into elements of Counter()
            if 'command' in object_methods:
                output_cntr += self.iterate_bashlex(bashlex_object.command)
            elif 'list' in object_methods:
                for element in bashlex_object.list:
                    output_cntr += self.iterate_bashlex(element)
            elif 'parts' in object_methods:        
                # if parts have parts within - go deeper 
                # (Leo from Inception looking at you)
                if bashlex_object.parts:
                    for part in bashlex_object.parts:
                        output_cntr += self.iterate_bashlex(part)
                else:
                    output_cntr = self.parse_word(bashlex_object, output_cntr)
            elif 'word' in object_methods:
                output_cntr = self.parse_word(bashlex_object, output_cntr)
            # Working on default specific types
            elif 'value' in object_methods:
                output_cntr[bashlex_object.value] += 1
            elif "pipe" in object_methods:
                output_cntr[bashlex_object.pipe] += 1
            elif "op" in object_methods:
                output_cntr[bashlex_object.op] += 1
            elif "type" in object_methods:
                output_cntr[bashlex_object.type] += 1
            else:
                if self.debug:
                    print("{DEBUG} Weird case - not parsed correctly:", bashlex_object)
                    import pdb; pdb.set_trace()
        
        return output_cntr


    def parse_word(self, bashlex_object, output_cntr):
        size = 1
        
        # Trying to parse input object again
        # helps if previous parse iteration didn't handled
        # some fragments of command (e.g. $(), ``, embedded ones)
        word = re.sub(r"[<>#{}]", "", bashlex_object.word).strip()
        if len(bashlex_object.word) > 20:
            p = self.bashlex_wrapper(word, output_cntr)
            if p:
                try:
                    size = len(p[0].parts)
                except AttributeError:
                    size = len(p[0].list)
        
        # if size > 1 then parsing found something new
        if size > 1:
            for node in p:
                output_cntr += self.iterate_bashlex(node)
            return output_cntr
        
        # if no new elements - improve bashlex parsing of flags w/ '='
        if '=' in bashlex_object.word and \
        '==' not in bashlex_object.word:
            l = bashlex_object.word.split('=')
            # special case
            if 'chmod' in bashlex_object.word.lower():
                output_cntr[l[0]] += 1
                output_cntr['='.join(l[1:])] += 1
            # standard 'flag=value' case
            elif len(l) == 2:
                output_cntr[l[0]] += 1
                output_cntr[l[1]] += 1
            # weird combination - add as is
            else:
                output_cntr[bashlex_object.word] += 1
 
        # bashlex parsing correct
        else:
            output_cntr[bashlex_object.word] += 1
        return output_cntr
    
    def parse(self, data):
        l = len(data)
        alldict = Counter()
        for i,command in enumerate(data):
            if self.verbose:
                print(f"[!] Parsing in process.. {i}\{l}", end="\r")
            nodes = self.bashlex_wrapper(command, alldict)
            if nodes:
                for node in nodes:
                    alldict += self.iterate_bashlex(node)
        return alldict