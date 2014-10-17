import sys
  

class Node:
  """ 
    One node of the parse tree.
    It is a group of words of same NamedEntityTag (e.g. George Washington).    
  """
  def __init__(self, word_list, namedentitytag='undef', dependency='undef', subnodes=[]):
    self.words = word_list      # List of words for this node (generally of size 1, at most 2 or 3)
    self.tag = namedentitytag   # String for the NamedEntityTag (e.g. 'PERSON' or 'DATE')
    self.dep = dependency       # Relation with the parent node (e.g. 'nn' or 'det' or 'root')
    self.child = subnodes       # List of children nodes
                                # parent attribute will be available after computaiton of the tree
                                
  def string(self):
    # Concatenation of the words of the root
    w = ''
    for x in self.words:
      w += x[:x.rindex('-')] + ' '
    w = w[:len(w)-1]
    s=''
    # Adding the definition of the root (dot format)
    t=''
    if(self.tag != 'O' and self.tag != 'undef'):
      t+= " ["+self.tag+"]"
    s+="\t\"{0}\"[label=\"{1}{2}\",shape=box];\n".format(self.words[0],w,t)
    # Adding definitions of the edges
    for n in self.child:
      s+="\t\"{0}\" -> \"{1}\"[label=\"{2}\"];\n".format(self.words[0],n.words[0],n.dependency)
    # Recursive calls
    for n in self.child:
      s+=n.string()+'\n'
    return s
    
  def __str__(self):
    return 'digraph relations {\n'+self.string()+'}\n'     

def compute_tree(r):
  """
    Compute the dependence tree.
    Take in input a piece of the result produced by StanfordNLP.
    If foo is this result, then r = foo['sentences'][0]
    Return the root of the tree (word 'ROOT-0').
  """
  name_to_nodes = {} # map from the original string to the node
  # Computation of the edges of the tree
  for edge in r['indexeddependencies']:
    try:
      n1 = name_to_nodes[edge[1]]
    except KeyError:
      n1 = Node([edge[1]])
      name_to_nodes[edge[1]] = n1
    try:
      n2 = name_to_nodes[edge[2]]
    except KeyError:
      n2 = Node([edge[2]])
      name_to_nodes[edge[2]] = n2
    # n1 is the parent of n2
    n1.child = n1.child+[n2]
    n2.parent = n1
    n2.dependency = edge[0]
  index=1
  # Computation of the tags of the nodes
  for word in r['words']:
    if word[0].isalnum() or word[0] == '$' or  word[0] == '%':
      w=word[0]+'-'+str(index) # key in the name_to_nodes map
      index+=1
      try:
        n = name_to_nodes[w]
        n.tag = word[1]['NamedEntityTag']
      except KeyError:        # this node does not exists (e.g. 'of' preposition)
        pass
  return name_to_nodes['ROOT-0']
  
  
