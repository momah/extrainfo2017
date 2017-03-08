#python movies.py movies.csv | sort
import MapReduce
import sys

"""
Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    if float(0 if record[3] is '' else record[3])>4:
      mr.emit_intermediate(key, value)


def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    mr.emit((key, list_of_values))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
