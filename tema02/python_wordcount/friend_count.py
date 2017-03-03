#execute as:
#python friend_count.py friends.json
#

import MapReduce
import sys

"""
Inverted index Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    
    -- Complete the code of mapper --
    -- Hint: mr.emit_intermediate(<key>, <value>)


def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    
    -- Complete the code of reducer --
    -- Hint: mr.emit((<key>, <operation with list_of_values>))


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)


