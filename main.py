import code_analyzer as ca

import os


# check if one file or many

# one file:
ca.analyse_code('./res/heapsort.py', True, True)

# many files
# go trough all files and find the .py files and add to an str
path = ""
complete_py_str = ""
entities = os.listdir(path)
# recursive is better for that
for entity in entities:
    pass
