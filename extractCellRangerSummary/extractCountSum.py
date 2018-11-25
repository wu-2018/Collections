import os
from collections import OrderedDict
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path-file', '-p', required = True, help = 'Specify the file containing path of each cellranger folder')
parser.add_argument('--output-filename', '-o', required = True, help = 'output filename')
parser.add_argument('--sep', '-s', default='\t', help = 'Separation character, e.g., "\t" or "," ')
args = parser.parse_args()                          
pathFile = args.path_file
filename = args.output_filename
sep = args.sep

with open(pathFile, "r") as f:
    pathLi = f.read().splitlines()

# ruling out commented lines
pathLi = [path for path in pathLi if not path.startswith('#') ]
print("Total sample number: ", len(pathLi))

totalLi = []
for index,path in enumerate(pathLi):
    htmlFile = os.path.join(path, "outs/web_summary.html")
    with open(htmlFile, "r") as f:
        bs = BeautifulSoup(f, "lxml")   
    di = OrderedDict()
    infoTable = bs.find_all("table", {"class":""})
    for i in infoTable:
        rows = i.find_all("tr")
        for row in rows:
            td = row.find_all("td")
            di[td[0].text] =  td[1].text           
    totalLi.append(di)

dictKeys = list(totalLi[0].keys())
# select highlighted keys that will be placed in the first serveral columns
hl_keys = ['Name', 'Estimated Number of Cells', 'Mean Reads per Cell', 'Median Genes per Cell']
sortedKeys = hl_keys + [i for i in dictKeys if i not in hl_keys]

def writeFile(filename, sep):
    with open(filename, "w+") as f:
        f.write(sep.join(sortedKeys)+'\n')
        
        for i in totalLi:
            values = [i[k] for k in sortedKeys]
            f.write(sep.join(values))       
            f.write('\n')
    return None
    
writeFile(filename, sep)
