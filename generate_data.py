import csv
import random as r


def getRandomRow(id_row, r):
  return id_row[id_row.keys()[int(r.random()*len(id_row))]]

def createTrainingSet(id_row, full_id_row, usedUri, r, amount):

  """
  Create Training Dataset extracting random pair of uri/(context,answer)
  with 50% right and 50% wrong
  """
  
  nbIdRequired = amount * len(id_row)
  
  result = []
  while len(result) < nbIdRequired/2:
    newRow = dict()
    row = getRandomRow(id_row, r)  
    
    if row["uri"] in usedUri:
      continue
    #id_row.pop(row["uri"])
    
    usedUri.add(row["uri"])
    newRow["uri"] = row["uri"]
    newRow["question"] = row["subject"]+" "+row["content"]
    newRow["bestanswer"] = row["bestanswer"]
    newRow["label"] = "0"
    result.append(newRow)
    
    print str(len(result))+"\r",
    
  while len(result) < nbIdRequired:
  
    newRow = dict()
    row = getRandomRow(id_row, r)

    if row["uri"] in usedUri:
      continue
    id_row.pop(row["uri"])
    
    usedUri.add(row["uri"])
    newRow["uri"] = row["uri"]
    newRow["question"] = row["subject"]+" "+row["content"]
    rRow = getRandomRow(full_id_row, r)
    while rRow == row:
      rRow = getRandomRow(full_id_row, r)
    
    newRow["bestanswer"] = rRow["bestanswer"]
    newRow["label"] = "1"  
    result.append(newRow)
    
    print str(len(result))+"\r",
    
  header = ["uri", "question", "bestanswer", "label"]
  return (header,result)

def createValTestSet(id_row, full_id_row, usedUri, r, amount):

  """
  Create a validation set and a test set with what was not used for the training set
  """  
  
  nbIdRequired = amount * len(id_row)
  nbDistractor = 9

  result = []
  while len(id_row)>0 and len(result) < nbIdRequired:
    newRow = dict()
    row = getRandomRow(id_row, r)

    if row["uri"] in usedUri:
      continue
    id_row.pop(row["uri"])

    usedUri.add(row["uri"])
    newRow["uri"] = row["uri"]
    newRow["question"] = row["subject"]+" "+row["content"]
    newRow["bestanswer"] = row["bestanswer"]
    for x in range(nbDistractor):
      s = set()
      s.add(newRow["uri"])
      rRow = getRandomRow(full_id_row,r)
      while rRow["uri"] in s:
        rRow = getRandomRow(full_id_row,r)
      newRow["distractor"+str(x)] = rRow["bestanswer"]
      
    result.append(newRow)

    print str(len(result))+"\r",

  header = ["uri", "question", "bestanswer"]
  for x in range(nbDistractor):
    header.append("distractor"+str(x))
  return (header, result)

if __name__ == "__main__":

  id_row = dict()
  full_id_row = dict()
  usedUri = set()
  amountTraining = 0.8  
  
  print "Reading data..."
  with open("data/clean_manner_print.csv") as f:
  
    csvReader = csv.DictReader(f)
    
    for row in csvReader: 
      if len(row["subject"])+len(row["content"]) > 50:
        id_row[row["uri"]] = row
        full_id_row[row["uri"]] = row
         
  print "{} lines loaded...".format(len(id_row))       
  r.seed(10)
  
  print "Start creating train data..."
  #with open("data/train.csv", "w") as fTrain:
  #  print "Generate train data with {}% of total data...".format(amountTraining*100)
  #  (header, data) = createTrainingSet(id_row, full_id_row, usedUri, r, amountTraining)
  #  csvWriter = csv.DictWriter(fTrain, header, extrasaction="ignore")
  #  csvWriter.writeheader()
  #  
  #  r.shuffle(data)
  #  print "Write training file..."
  #  csvWriter.writerows(data)
  
  print "Start creating validation set..."
  with open("data/valid.csv", "w") as fVal:
    print "Generate valid data with {}% of the total data...".format((1-amountTraining)*50)
    (header, data) = createValTestSet(id_row, full_id_row, usedUri, r, (1-amountTraining)/2)
    csvWriter = csv.DictWriter(fVal, header, extrasaction="ignore")
    csvWriter.writeheader()

    r.shuffle(data)
    print "Write validation file..."
    csvWriter.writerows(data)
  
  print "Start creating test set..."
  with open("data/test.csv", "w") as fTest:
    print "Generate test data with {}% of the total data...".format((1-amountTraining)*50)
    (header, data) = createValTestSet(id_row, full_id_row, usedUri, r, 1-amountTraining)
    csvWriter = csv.DictWriter(fTest, header, extrasaction="ignore")
    csvWriter.writeheader()

    r.shuffle(data)
    print "Write test file..."
    csvWriter.writerows(data)

    
