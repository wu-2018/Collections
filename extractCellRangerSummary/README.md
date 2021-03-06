# 

***
*Until this script has been finished, I found a `metrics_summary.csv` locating under the same folder with `web_summary.html`, so actually there's no need to extract information from the html.*
  
*Admittedly I've taken a detour. But anyway, this script can equally work and I've trained my python crawler skills again.*
  
***

[Cell Ranger](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/what-is-cell-ranger) is a powerful tool for processing scRNA-seq data from 10xGENOMICS platform.
  
Everytime when `cellranger count` finished, it automatically generates a html report, named `web_summary.html`.
  
![CRwebsum](websum.png)

But this human-friendly web report are not so efficient when we got many scRNA-seq samples, i.e., we have to check all the reports one by one.
  
So here I present this little script capable of extracting key information from multiple Cell Ranger web reports. 
  
Usage: 
`python3 extractCountSum.py -p pathFile -o outputFileName -s \t`
  
- `-p` Specify the file containing path of each cellranger, one path per line, e.g.:
  
```
#path.txt
~/CellrangerCount/PC20180703ABC
~/CellrangerCount/PC20180703XYZ
~/CellrangerCount/PC20180703OPQ
```
  
- `-o` Specify the output file name
- `-s` Optional separation character, default is `\t`, i.e, a `tsv` file
  
e.g., `python3 extractCountSum.py -p path.txt -o total.tsv`
  
