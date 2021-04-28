# OCR
Repo for OCR detection system
Before running the .py code, run:
```
!apt-get install ocrmypdf -q

!pip install pdfplumber -q

!pip3 install img2pdf
```

Function call:
E.g, transcript_call(x,y,z): variable x is the URL link to the transcript; variable y is either "signup" or "grade" where "signup" returns the First/Last Name along with the Level of Education and "grade" just returns the grade of the class name that is in variable z.

Example call:
transcript_call("https://work.fibonia.com/1/html/uploadstranscript/transcript.pdf","signup","INDENG 242"), in this case "INDENG 242" (aka variable z) would not matter and can be left blank since "signup" does not require the course name.
