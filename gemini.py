from pypdf import PdfReader
import google.generativeai as genai
import customtkinter as ctk

import markdown
from tkinter import filedialog as fd
import tkinter as tk
import tkinter.font as tkfont
import tkinter.scrolledtext as tkscroll
from tkhtmlview import HTMLLabel
from tkinter import ttk

genai.configure(api_key="AIzaSyB5hVO3WufQ6M-hJSrOBgKvYtKKIUJL6Cc")
ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

fileName = ""

def to_markdown(text):
  text = text.replace('•', '  *')
  return markdown.markdown(text, output_format="html")

def selectFile():
  global fileName
  filetypes = (
        ('PDF files', '*.pdf'),
        ('All files', '*.*')
    )

  fileName = fd.askopenfilename(title='Open files', filetypes=filetypes)
  labelFile.configure(text=f"File Selected : \"{fileName}\"")

def generateResponse():
  
  reader = PdfReader(fileName)
  
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content(f"Ecris {entryThema.get("1.0", ctk.END)} en reprenant le style d'écriture listé dans le texte suivant : {reader.pages[0].extract_text()}")
  
  outputText.configure(state="normal")
  outputText.insert("0.0", response.text)
  outputText.configure(state="disabled")
  outputHTML.set_html(to_markdown(response.text))

window = ctk.CTk()
window.geometry("1080x480")
sideBar = ctk.CTkFrame(window)
sideBar.pack(side="left", expand=True)

bottomZone = ctk.CTkFrame(window, width=window.winfo_screenwidth())
bottomZone.pack(side = "bottom", expand=True)

centerZone = ctk.CTkFrame(window)
centerZone.pack(side="right", expand=True)

titleFrame = ctk.CTkFrame(sideBar)
titleFrame.pack(side="top", expand=True)
title = ctk.CTkLabel(titleFrame, text="Générateur de Dissertations", font=("Segoe UI", 16))
title.pack(side="top")
subtitle = ctk.CTkLabel(titleFrame, text="Par Marsisus")
subtitle.pack(side = "bottom")

buttonSide = ctk.CTkButton(sideBar, command=selectFile, text="Sélectionner un exemple")
buttonSide.pack(side=ctk.BOTTOM)

labelFile = ctk.CTkLabel(sideBar, text="File Selected : \"\"")
labelFile.pack(side= "bottom")

inputFrame = ctk.CTkFrame(centerZone)
inputFrame.pack(side="top")

entryTitle = ctk.CTkLabel(inputFrame, text="Entrez ici ce que vous souhaitez générer: ")
entryTitle.pack(side="top")
entryThema = ctk.CTkTextbox(inputFrame, width=centerZone.winfo_screenwidth(), height=120)
entryThema.pack(side="left", expand=True)

outputFrame = ctk.CTkFrame(centerZone)
outputFrame.pack(side="bottom", expand=True)

tabview = ctk.CTkTabview(outputFrame)
tabview.pack(expand=True)
tab_out = tabview.add("Sortie Texte")  # add tab at the end
tab_html = tabview.add("Sortie Formatée")  # add tab at the end

outputText = ctk.CTkTextbox(tab_out, width=centerZone.winfo_screenwidth(), height=400)
outputText.configure(state="disabled")
outputText.pack(expand=True)

outputHTML = HTMLLabel(tab_html, width=centerZone.winfo_screenwidth())
outputHTML.pack(expand=True)




validate = ctk.CTkButton(bottomZone, command=generateResponse, text="Générer")
validate.pack(side="right", expand=True, pady=10, anchor="se")


window.mainloop()
