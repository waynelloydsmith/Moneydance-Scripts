#!/usr/bin/env python
# coding: utf8
#import sys
#import subprocess
#subprocess.call(['./abc.py', arg1, arg2])
#os.system
#os.spawn*
#os.popen*
#popen2.*
#commands.*
#sys.argv.append("--help")
#sys.argv.remove(value) -- remove first occurrence of value.
#sys.argv._contains_('-x')
#sys.argv._len_('-x') same as len (sys.argv)
#sys.argv.append('-x')-- append object to end
#sys.argv.count(value) -> integer -- return number of occurrences of value
#sys.argv.extend(iterable) -- extend list by appending elements from the iterable
#sys.argv.index(value, [start, [stop]]) -> integer -- return first index of value.
#        idx = sys.argv.indexOf('-x')
#sys.argv.insert(index, object) -- insert object before index
#sys.argv.pop([index]) -> item -- remove and return item at index (default last).
#                  opt = sys.argv.pop(1)
#sys.argv.remove(value) -- remove first occurrence of value.
#sys.argv.reverse('-x')-- reverse *IN PLACE*

# argv[o] is empty 
#load the arguments prior to the call with append
#program must unload them or they will accumulate use pop or remove
import sys
#first  =  sys.argv[0]
#second = sys.argv[1]
#third = sys.argv[2]
arglen = len(sys.argv)
print 'number of arguments=' , arglen - 1
i = 1
while ( i < arglen ):
  value = sys.argv.pop()
  print i,value
 # sys.argv.remove(value) messes up list
  i = i + 1

  
  
# opt = sys.argv.pop(1)  
  
