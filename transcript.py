import os
import json
import requests
import pdfplumber
import json
def transcript_call(url1,req,ourclass=0):
  def download_file(url):
      local_filename = url.split('/')[-1]
      headers = {'User-Agent': 'XY', 'Content-type': 'application/json'}
      with requests.get(url,headers=headers) as r:
          assert r.status_code == 200, f'error, status code is {r.status_code}'
          with open(local_filename, 'wb') as f:
              f.write(r.content)
      return local_filename
  invoice = url1
  invoice_pdf = download_file(invoice)
  try:
    with pdfplumber.open(invoice_pdf) as pdf:
        os.remove(invoice_pdf)
        page = pdf.pages[0]
        text = page.extract_text(x_tolerance=2)
        lines = text.split('\n')
        firstname = ""
        secondname = ""
        lvl = ""
        grade=""
        if req == "grade":
          for line in lines:
            if ourclass in line:
              grade = line.split(' ')[-2]
          if grade == "":
            return None
          else:
            return json.dumps({"grade":grade})
        elif req == "signup":
          for line in lines:
            if "Name " in line:
              firstname = line.split(' ')[1]
              lastname = line.split(' ')[-1]
            if "Level " in line:
              lvl = line.split(' ')[-1]
          if firstname == "" or lastname=="" or lvl == "":
            return None
          else:
            return json.dumps({"firstname":firstname,"lastname":lastname,"lvl":lvl})
        else:
          return None
  except:
    return "ERROR"

x = transcript_call("http://www.work.fibonia.com/1/html/uploadstranscript/5fa91e4b8d63f3.16225769.pdf","grade","INDENG 290")
x