import os
import json
import requests
import pdfplumber
import json
import img2pdf
import urllib.request
from PIL import Image
def transcript_call(url1,req,ourclass=0):
  def download_file(url):
      local_filename = url.split('/')[-1]
      headers = {'User-Agent': 'XY', 'Content-type': 'application/json'}
      with requests.get(url,headers=headers) as r:
          assert r.status_code == 200, f'error, status code is {r.status_code}'
          with open(local_filename, 'wb') as f:
              f.write(r.content)
      return local_filename
  if url1[len(url1)-3:len(url1)] != "pdf":
    invoice_pdf = "tstoutput.pdf"
    if url1.split('.')[-1] == "JPG":
      ourfile = "tstyes.JPG"
      urllib.request.urlretrieve(url1, "tstyes.JPG")
    else:
      ourfile = "tstyes.PNG"
      urllib.request.urlretrieve(url1, "tstyes.PNG")
    image = Image.open(ourfile) 
    pdf_bytes = img2pdf.convert(image.filename) 
    file = open(invoice_pdf, "wb") 
    file.write(pdf_bytes) 
    image.close() 
    file.close()
    os.remove(ourfile)
  if url1[len(url1)-3:len(url1)] == "pdf":
    invoice = url1
    invoice_pdf = download_file(invoice)
  url1 = invoice_pdf 
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
        for i in range(0,len(pdf.pages)):
          page = pdf.pages[i]
          text = page.extract_text(x_tolerance=2)
          lines = text.split('\n')
          for line in lines:
            if "My Academics" in line:
              ourbool = True
              break;
            else:
              ourbool = False
        if req == "grade":
          for i in range(0,len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text(x_tolerance=2)
            lines = text.split('\n')
            for line in lines:
              if ourclass in line and ourbool == False:
                grade = line.split(' ')[-2]
              elif ourclass in line and ourbool:
                grade = line.split(' ')[-1]
          if grade == "":
            return None
          else:
            return json.dumps({"grade":grade})
        elif req == "signup":
          for i in range(0,len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text(x_tolerance=2)
            lines = text.split('\n')
            for line in lines:
              if ourbool == False:
                if "Name " in line:
                  firstname = line.split(' ')[1]
                  lastname = line.split(' ')[-1]
                if "Level " in line:
                  lvl = line.split(' ')[-1]
              elif ourbool:
                firstname = lines[3].split(' ')[0]
                lastname = lines[3].split(' ')[-1]
                lvl = [lines[x].split(' ')[-1] for x in range(0,len(lines)) if  "Level " in lines[x]]
                break;
            break;
          if firstname == "" or lastname=="" or lvl == "":
            return None
          else:
            return json.dumps({"firstname":firstname,"lastname":lastname,"lvl":lvl})
        else:
          return None
  except Exception as e:
    return None

x = transcript_call("https://work.fibonia.com/1/html/uploadstranscript/transcript.pdf","signup","INDENG 242")
x
