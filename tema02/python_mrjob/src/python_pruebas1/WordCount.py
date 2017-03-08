'''
Created on 9 de ago. de 2015

@author: hduser
'''

'''
#ejecutar en local
python src/python_pruebas1/WordCount.py input3/README.rst > output/out.txt
python src/python_pruebas1/WordCount.py input3/README.rst -o output

# ejecutar en AWS EMR
python src/python_pruebas1/WordCount.py input3/README.rst -r emr > counts

# ejecutar en Hadoop cluster
hadoop fs -mkdir inputs/input3
hadoop fs -put input3/README.rst inputs/input3/
hadoop fs -rm -r -f output

python src/python_pruebas1/WordCount.py hdfs:///user/hduser/inputs/input3/README.rst -r hadoop > output/out.txt
python src/python_pruebas1/WordCount.py hdfs:///user/hduser/inputs/input3/README.rst -r hadoop -o output
hadoop fs -cat output/*
'''
    
"""The classic MapReduce job: count the frequency of words.
"""
from mrjob.job import MRJob
import re

#from pywebhdfs.webhdfs import PyWebHdfsClient
#hdfs = PyWebHdfsClient(host='localhost',port='50070', user_name='hduser')
#dir=hdfs.list_dir('/')
#print json.dumps(dir,indent=4)
#hdfs.delete_file_dir('/user/hduser/output')

WORD_RE = re.compile(r"[\w']+")


class MRWordFreqCount(MRJob):

    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))


if __name__ == '__main__':
    MRWordFreqCount.run()
    
    
    
    