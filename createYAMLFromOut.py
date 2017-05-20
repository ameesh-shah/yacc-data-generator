import yaml
import re
import string
import sys

'''
HOW TO USE:
This program is meant to take an out file, created by calling yyextract on a YACC file
that has specified grammar, and create a YAML file that parses the .out file so that the
user can see the rules in a hierarchical manner and input the probability distributions within the YAML.

USAGE: Usage for this program is pretty straightforward. on the command line, call createYAMLFromOut.py with
two arguments: the first is the raw outfile that was produced when yyextract was called on the yacc file.
The second should be the location where you want the yaml file (a blank .yaml file is perfectly fine.)
EXAMPLE:

python createYAMLFromOut.py "grammar.out" "grammar.yaml" 
(assuming these two files already exist)

Best of luck!

author ameeshshah
'''

class PrettySafeLoader(yaml.SafeLoader):
    '''
    safe loader for the yaml to not mess up formatting.
    '''
    def construct_python_tuple(self, node):
        return tuple(self.construct_sequence(node))

def create_yaml_from_out(outfile):
    '''
    :param outfile: the raw outfile produced by yyextract.
    :return: a dictionary that can be sent to the yaml tool (imported) to create an accurate yaml file.
    '''
    master_yaml_dict = {}
    tokendict = {}
    lhsdict = {}
    lhslist = []
    tokenlines = []
    with open(outfile, "r") as myFile:
        useOutfile = myFile.readlines()

    for line in useOutfile:
        splitline = line.split()
        if len(splitline) != 0:
            #finds and adds tokens
            if splitline[0] == "%token":
                tokenlines.append(splitline)
        if len(splitline) == 1:
            lhs_regex = '[a-zA-Z_][a-zA-Z_0-9]*:'
            matchMe = re.search(lhs_regex, splitline[0])
            if matchMe is not None:
                #finds and adds lhses
                currentlhs = matchMe.group(0)
                addlhs = currentlhs.replace(":", "")
                lhslist.append(addlhs)



    for tokenline in tokenlines:
        for i in range(len(tokenline)):
            if i != 0:
                #adds sample space for realizations and space for their probabilities
                tokendict[tokenline[i]] = {"Realization Goes Here" : "Realization Probability Goes Here"}
    #formatting the string to add rhs
    useOutfileString = ''.join(useOutfile)
    useOutfileString = useOutfileString.replace('\n', '')
    useOutfileString = useOutfileString.replace(';', ';\n')
    useOutfileString = useOutfileString.replace('\t', ' ')
    fullNameStringList = []
    for lhs in lhslist:
        regexString = lhs+':.*;'
        matchMe = re.search(regexString, useOutfileString)
        if matchMe is not None:
            fullNameStringList.append(matchMe.group(0))
        else:
            regexString = lhs+'.*::=.*'
            matchMe = re.search(regexString, useOutfileString)
            fullNameStringList.append(matchMe.group(0))

    for expansion in fullNameStringList:
        #print expansion + "\n"
        for lhs in lhslist:
            #splits up each separate RHS
            stepexpansion = re.split(': | \|', expansion)
            if lhs in stepexpansion[0] and len(lhs) == len(stepexpansion[0]):
                rhsdict = {}
                for i in range(len(stepexpansion)):
                    if i != 0:
                        #different formatting for empty
                        if "/* empty */" in stepexpansion[i]:
                            rhsdict["empty"] = "Insert RHS Probability Here"
                        else:
                            rule = stepexpansion[i].split(" ")
                            realrule = []
                            for token in rule:
                                #chops off quotes from specific tokens
                                if token.startswith("'") and token.endswith("'"):
                                    token = token[1:-1]
                                if token != '' and token != ';':
                                    realrule.append(token)
                            if stepexpansion[i][-1] == ';':
                                cleanexpansion = stepexpansion[i][1:-1]
                            else:
                                cleanexpansion = stepexpansion[i][1:]
                            #final formatting before the RHSs are correct
                            finalexpansion = cleanexpansion.rstrip(string.whitespace)
                            finalexpansion = finalexpansion.replace("'", "")
                            #space for the RHS probabilities
                            rhsdict[finalexpansion] = "Insert RHS Probability Here"
                #additional space to add the LHS starting probabilities
                rhsdict["LHS PROBABILITY:"] = "Insert LHS Probability Here"
                lhsdict[lhs] = rhsdict

    ###TESTING###
    #print "TOKEN DICT: " + tokendict.__str__()
    #print "LHS LIST: " + lhslist.__str__()
    #print "UseOutfileString: " + useOutfileString
    #print "Full Name String List: " + fullNameStringList.__str__()
    #print fullNameStringList.__len__()
    #print "LHS DICT: " + lhsdict.__str__()
    #############

    #puts them in the master dict that can then be passed to the yaml tool
    master_yaml_dict["Tokens"] = tokendict
    master_yaml_dict["LHS"] = lhsdict
    return master_yaml_dict



def generate_yaml(master_dict, yamlfile):
    '''
    :param master_dict: the dictionary produced by create_yaml_from_out
    :param yamlfile: the location where the yaml file will be produced
    :return: a properly filled up yaml file
    '''
    with open(yamlfile, 'w') as f:
        yaml.safe_dump(master_dict, f, default_flow_style=False)



if __name__ == "__main__":
    #get arguments from the command line
    arguments = sys.argv
    #first input is the raw out file, second is the yaml file
    outfile = arguments[1]
    yamlfile = arguments [2]
    #call functions to generate the yaml file that the user can fill up with probability distributions
    dicttouse = create_yaml_from_out(outfile)
    generate_yaml(dicttouse, yamlfile)

