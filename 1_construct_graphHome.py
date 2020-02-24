

from graphviz import Digraph
import itertools


#TRAINING
# INPUT_FILE= 'data/with_indicators_train-consistent.tsv'
# OUTPUT_FILE= 'training'
#VALIDATION
# INPUT_FILE= 'data/validation_n_training.tsv'
# OUTPUT_FILE= 'validation'
#POLICY
INPUT_FILE= 'tokens.txt'
OUTPUT_FILE= 'policy'



dot = Digraph(comment='TA Pair',strict=True,graph_attr=dict(pad="0.5", nodesep="1", ranksep="10",size="12,12"))

def findsubsets(S,m):
    return list(itertools.combinations(S, m))
    
def has_edge(graph, v1, v2):
    tail_name = graph._quote_edge(v1)
    head_name = graph._quote_edge(v2)
    return (graph._edge % (tail_name, head_name, '')) in graph.body

def consider_all_subsets(a_token):
    elements = a_token.replace('<','').replace('>','').split(',')
    node_string = ''
    l_node_string = []
    final_list_subsets = []
    for i in range(0,len(elements[0].split('-'))):
        
        node_string = '<' +  elements[0].split('-')[i] + ',' +  elements[1].split('-')[i]  + ','+  elements[2].split('-')[i] + '>'
        l_node_string.append(node_string)
    # print('---->',l_node_string)
    for i in range(1,len(l_node_string)+1):
        s_subset_nodes = findsubsets(l_node_string,i)
    
        # print("~~>",s_subset_nodes)
        
        for m in range(0,len(s_subset_nodes)):
            device= '<'
            capability = ''
            action = ''
            for k in s_subset_nodes[m]:
                # print()
                # print("<~~~>",k)
                device += k.split(',')[0].replace('<','') + '-'
                capability +=k.split(',')[1] + '-'
                action+= k.split(',')[2].replace('>','') + '-'

            new_token = device[:-1] + ',' + capability[:-1] + ',' + action[:-1] + '>'
            # print('<---',new_token)
            final_list_subsets.append(new_token)
    return final_list_subsets

def get_subtokens(token, d_all_tokens):
    if(token not in d_all_tokens.keys()):
            d_all_tokens[token] =[token]

    if ('-' in token): # AND FOR ACTION_ITEMS.
        l_subsets = consider_all_subsets(token) # Consider all subtokens
        # print(l_subsets)
        for node_string in l_subsets:
            if(node_string not in d_all_tokens[token]):
                d_all_tokens[token].append(node_string)
    return d_all_tokens


def extract_subset_dictionaries(input_file):
    d_all_t_tokens = {}
    d_all_a_tokens = {}
    with open(input_file,'r') as fromFile:
        next(fromFile)
        for line in fromFile:
            cols = line.split()
            t_token = cols[0]
            a_token = cols[1]

            d_all_t_tokens = get_subtokens(t_token,d_all_t_tokens)
            d_all_a_tokens = get_subtokens(a_token, d_all_a_tokens)

    return d_all_t_tokens, d_all_a_tokens










# Each Key is a Token and the Value are the list of subset of tokens possible.
d_all_t_tokens,d_all_a_tokens = extract_subset_dictionaries(INPUT_FILE)


# An Action Being Triggered by Other Triggers
# E.g., {'A-B':c, 'A':d} Here, there should be edge from 'A-B' to d
with open(INPUT_FILE,'r') as fromFile:
    # next(fromFile)
    for line in fromFile:
        cols = line.split()
        t_token = cols[0]
        a_token = cols[1]
        
        # Which other trigger token leads to the current action?
        # In this case if the subset of the trigger token matches any other trigger token, we define edge
        for k,v in d_all_t_tokens.items():
            if t_token in v: # If trigger token is present in one of the values array
                if not has_edge(dot,k,a_token):
                    if(k != a_token):
                        print('ORIGINAL: ', t_token, ' --> ', a_token)
                        print('Now: ',k,' ---> ',  a_token)
                        dot.edge(k,a_token) # Because we already created the nodes
                        break
print('----')

# A Trigger Being Triggered by Part Of Actions
# E.g., {'A-B':c, 'A':d} Here, there should be edge from 'A-B' to d
with open(INPUT_FILE,'r') as fromFile:
    # next(fromFile)
    for line in fromFile:
        cols = line.split()
        t_token = cols[0]
        a_token = cols[1]

        # Which other actions token leads to the current trigger
        # In this case if the subset of the action token matches any trigger token, we define edge
        for k,v in d_all_a_tokens.items():
            for subset_action in v:
                if subset_action == t_token:
                    if not has_edge(dot,k,t_token):
                        if(k != t_token):
                            dot.edge(k,t_token) # Because we already created the nodes
                            print('ORIGINAL: ', t_token, ' --> ', a_token)
                            print('Now: ',k,' ---> ',  a_token)
                            break

# print(dot.source)
with open('generated_data/dot_files/'+OUTPUT_FILE+'.dot','w') as toFile:
    toFile.write(dot.source)

dot.render('generated_data/graphs/'+OUTPUT_FILE + '-new.gv.pdf', view=True)  # doctest: +SKIP       

# WRITING
# COnsider trigger that can lead to other actions
# Consider Actions that can lead to other triggers