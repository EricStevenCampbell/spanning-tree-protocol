#!/usr/bin/env bash
# use provided validate script
# Note: please put all test files into the same folder as project scripts
# Topo name: *.py
# Answer name: *.txt (should be the same as Topo name)
# Your result name: *_my_result.txt

# Remove old output files.
rm *_my_result.txt

# For every file ending in *.txt, run "run_spanning_tree.py" and then run "ValidateAnswer.py".

for i in *.txt
do
    # Remove '.txt'
    name=$(echo $i | cut -f 1 -d '.')
    echo $name

    # Set output file name.
    outputFile=${name}_my_result.txt

    # Execute script and run diff.
    python run_spanning_tree.py $name $outputFile
    python ValidateAnswer.py -s $outputFile -r ${name}.txt   
done