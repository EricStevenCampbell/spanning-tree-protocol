# spanning-tree-protocol

### Description

This project implements a simplified distributed version of the Spanning Tree Protocol that can be run on an arbitrary layer 2 topology in computer networks.

The project simulated the communications between switches until they converge on a single solution, and then output the final spanning tree to a file.

### Usage
To run the code on a specific topology and output the results to a text file, please execute the following command:
```
python run_spanning_tree.py TopoName TopoNameOut.txt
```
You can also validate the output file using the standard output file:
```
python ValidateOutput.py -s TopoNameOut.txt -r TopoNameOutStandard.txt
```
Or, for conviniece, you can test using provided bash scripts `test_all.sh` to test all topologies. 
