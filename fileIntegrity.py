import os
import os.path
import json

def checkFiles(*paths):
    for filePath in paths:
        if not (os.path.isfile(filePath) and os.access(filePath, os.R_OK)):
            raise FileExistsError(f'check if {filePath} is readable and intact')
    print('-> filesystem intact')

def writeJson(data, filename):
    with open(f'intermediate_results/{filename}.json', 'w') as f:
        json.dump(data, f)