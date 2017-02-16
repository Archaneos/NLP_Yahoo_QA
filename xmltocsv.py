import csv, sys, re
import xml.etree.ElementTree as ET

def clean(string):
  if string is None or len(string) == 0:
    return ""
  string = re.sub("<br>","",string)
  string = re.sub("<br />", "", string)
  return ' '.join(string.splitlines()).lower()


outFile = open(''.join([sys.argv[1],".csv"]),"w")
columns = ["uri","subject", "content", "bestanswer"]
for i in range(10):
  columns.append(''.join(["answer_item",str(i)]))

outFileWrite = csv.DictWriter(outFile, columns, extrasaction="ignore")

root = ET.parse(''.join([sys.argv[1],".xml"]))

data = dict()

for elem in root.iter("vespaadd"):
 try:
  data["uri"] = elem.find("document").find("uri").text
  data["subject"] = clean(elem.find("document").find("subject").text)
  data["content"] = ""
  content = elem.find("document").find("content")  
  if content is not None:
    data["content"] = clean(elem.find("document").find("content").text)
  data["bestanswer"] = clean(elem.find("document").find("bestanswer").text)

  i=0
  for nba in elem.find("document").find("nbestanswers").findall("answer_item"):
    data["answer_item"+str(i)] = clean(nba.text)
    if i == 9:
      break
    i+=1
      
  if i < 9:
    while i < 10:
      data["answer_item"+str(i)] = ""
      i+=1
      
  outFileWrite.writerow(data)
 except AttributeError as details:
  print data["uri"]
  print elem
  print "Error: ",details
  exit() 
outFile.flush()
outFile.close()
    
