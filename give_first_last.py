import json
import sys

f = open(sys.argv[1])

j = json.load(f)
f.close()

list_of_ids = [int(i) for i in j]

print "File has ids from {} to {}".format(min(list_of_ids), max(list_of_ids))
