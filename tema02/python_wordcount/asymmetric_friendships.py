#python asymmetric_friendships.py friends.json
import MapReduce
import sys

"""
Inverted index Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # emit every combo of friends
    -- Complete the code of mapper --
    -- Hint: mr.emit_intermediate(<key1>, <value>) and mr.emit_intermediate(<key2>, <value>) for each pair of friends



def reducer(key, list_of_values):
    friends = []
    for value in list_of_values:
        -- Complete the code of reducer --
        -- Hint: Avoid repetition of friends

    for friend in friends:
        mr.emit((key, friend))


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

