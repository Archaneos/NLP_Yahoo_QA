import re
import sys

entities = {"&amp;":"&", "&lt;":"<", "&gt;":">", "&#xd;":" ","&#ad;":"", "&#xa;": "", "<br>":"", "<br />":""}

def subHTML(line):
  for (key,val) in entities.items():
    line = re.sub(key,val,line)
    
  return line

fout = open(sys.argv[2],"w")

with open(sys.argv[1], "r") as f:
  for line in f:
    fout.write(subHTML(line))
