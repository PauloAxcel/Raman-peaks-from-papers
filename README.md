# Raman-peaks-from-papers

Easy python code to look for peaks in your papers. Uses pytesseract package (related to tesseract from google) and pdf2image package as the main pdf read/interpret text package. Followed by a search for a specific key work, in this case cm, (which is relate to the Raman peak units, found in all papers). The code extracts the peak, the sentece where that value came, and 3 other columns ('height','importance' and 'width') that are irrelevante in this context but are useful for other ongoing work.

There are 3 important notes for this code to work you need to 1st install tesseract from https://github.com/UB-Mannheim/tesseract/wiki then pip install pytesseract 2nd install poppler from https://github.com/oschwartz10612/poppler-windows/releases/ 3rd download all your pdf files, that you want to extract the peak detailed information into, and put them into a folder

os.chdir(<your pdf files dir>) 
pytesseract.pytesseract.tesseract_cmd = <your tesseract.exe file dir (terminated in \tesseract.exe)>
poppler_path = <poppler bin dir>
