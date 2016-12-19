
'''
  Module for normalizing alchemy documents to have appropriate field types.
'''

def normalize_docSentiment(doc):
  doc['docSentiment']['score'] = float(doc['docSentiment']['score'])
  return doc

def normalize_taxonomy(doc):
  for i in range(len(doc['taxonomy'])):
    doc['taxonomy'][i]['score'] = float(doc['taxonomy'][i]['score'])
  return doc

def normalize_entities(doc):
  for i in range(len(doc['entities'])):
    doc['entities'][i]['relevance'] = float(doc['entities'][i]['relevance'])
    doc['entities'][i]['count'] = int(doc['entities'][i]['count'])
    if 'emotions' in doc['entities'][i]:
      for key in doc['entities'][i]['emotions'].keys():
        doc['entities'][i]['emotions'][key] = float(doc['entities'][i]['emotions'][key])  
  return doc

def normalize_docEmotions(doc):
  for key in doc['docEmotions'].keys():
    doc['docEmotions'][key] = float(doc['docEmotions'][key])
  return doc

def normalize_keywords(doc):
  for i in range(len(doc['keywords'])):
    doc['keywords'][i]['relevance'] = float(doc['keywords'][i]['relevance'])
    if 'emotions' in doc['keywords'][i]:
      for key in doc['keywords'][i]['emotions'].keys():
        doc['keywords'][i]['emotions'][key] = float(doc['keywords'][i]['emotions'][key])
  return doc

def normalize_concepts(doc):
  for i in range(len(doc['concepts'])):
    doc['concepts'][i]['relevance'] = float(doc['concepts'][i]['relevance'])
  return doc

def main(doc):
  doc = normalize_concepts(doc)
  doc = normalize_docSentiment(doc)
  doc = normalize_docEmotions(doc)
  doc = normalize_taxonomy(doc)
  doc = normalize_entities(doc)
  doc = normalize_keywords(doc)
  return doc
