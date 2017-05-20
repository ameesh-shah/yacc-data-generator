# yacc-data-generator
This repository is designed to take in a yacc file, specifying grammar rules for any language, and will produce random data based on those grammars in two easy steps. 

First, call yyextract on your YACC file to produce a standard .out file that doesn't have to be modified in any way. From there, usage instructions are in createYAMLFromOut.py (step 1.) 

Once the YAML file has been generated, you can input your probability distributions and feed it to generateDataFromYAML.py. See that python file (step 2) for usage instructions. \n Happy generating!
