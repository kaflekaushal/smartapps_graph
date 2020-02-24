import csv
import sys

# returns all trigger-action pairs
def gettriacts(file):
    alltriacts=[line[2].split('||') for line in file if line[2].strip()][1:]
    return alltriacts

#strips stray spaces
def formatter(triacts):
    for num,ta in enumerate(triacts):
        for n,pair in enumerate(ta):
            triacts[num][n]=pair.strip().replace('-','->')
    return triacts

#returns 2 sets, uniquetriggers and uniqueactions as well as a list containing all trigger-action pairs, all tokenized
def tokenizer(triacts):
    tokens=[]
    uniquetriggers=set()
    uniqueactions=set()
    for number,ta in enumerate(triacts):
        for num,pair in enumerate(ta):
            pair=[p.strip().split(' ') for p in pair.split('->')]
            token=''
            for n,p in enumerate(pair):
                if n:
                    if len(p)==2:
                        t='<'+p[0]+','+p[1]+'>'
                    else:
                        t='<'+p[0]+',active>'
                    token=token+' -> '+t
                    uniqueactions.add(t)
                else:
                    if len(p)==2:
                        t='<'+p[0]+','+p[1]+'>'
                    else:
                        t='<'+p[0]+',active>'
                    token=token+t
                    uniquetriggers.add(t)
            tokens.append(token)
    return uniquetriggers,uniqueactions,tokens

#writes the tokens, unique triggers and unique actions to separate files
def writeToFile(tokens,triggers,actions):
    with open('tokens.txt','w') as tokenfile:
        for t in list(set(tokens)):
            tokenfile.write(t+'\n')

    with open('uniquetriggers.txt','w') as triggerfile:
        for t in triggers:
            triggerfile.write(t+'\n')

    with open('uniqueactions.txt','w') as actionfile:
        for t in actions:
            actionfile.write(t+'\n')

def main():
    if len(sys.argv)!=2:
        print('Usage: python3 <script> <tsv_file>')
        return
    inputfile=open(sys.argv[-1],'r')
    formattedinput=csv.reader(inputfile,delimiter='\t')
    alltriacts=formatter(gettriacts(formattedinput))
    uniquetriggers,uniqueactions,tokens=tokenizer(alltriacts)
    writeToFile(tokens,uniquetriggers,uniqueactions)
    print(len(tokens),len(uniquetriggers),len(uniqueactions))

if __name__=='__main__':
    main()
