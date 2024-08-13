# import PyPDF2 as pypdf
# import pandas as pd
# pdfobject=open('/Users/jarvis/pymycod/automation/sp_scraper/academia_scraper/Academic Planner 2023-24 ODD.pdf','rb')
# pdf=pypdf.PdfFileReader(pdfobject)
# print(pdf.)


import PyPDF2
 
pdfFileObj = open('/Users/jarvis/pymycod/automation/sp_scraper/academia_scraper/Academic Planner 2023-24 ODD.pdf', 'rb')
pdfReader = PyPDF2.PdfReader(pdfFileObj)
print(len(pdfReader.pages))
pageObj = pdfReader.pages[0]
print(pageObj.extract_text())
 
