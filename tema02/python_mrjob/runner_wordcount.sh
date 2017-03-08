echo '#ejecutar en local'
#python src/python_pruebas1/WordCount.py input3/README.rst > output/out.txt
python src/python_pruebas1/WordCount.py input3/README.rst -o output

# ejecutar en AWS EMR
#python src/python_pruebas1/WordCount.py input3/README.rst -r emr > counts

echo '# ejecutar en Hadoop cluster'
#hadoop fs -mkdir inputs/input3
#hadoop fs -put input3/README.rst inputs/input3/
hadoop fs -rm -r -f output

#python src/python_pruebas1/WordCount.py hdfs:///user/hduser/inputs/input3/README.rst -r hadoop > output/out.txt
python src/python_pruebas1/WordCount.py hdfs:///user/hduser/inputs/input3/README.rst -r hadoop -o output
hadoop fs -cat output/*
