import streamlit as st
import subprocess
from subprocess import STDOUT
import os
import base64
import camelot as cam
import pandas as pd
import tkinter as tk
from io import BytesIO
from xlsxwriter import Workbook

st.set_page_config(page_title="Cyberakash's PDF to Excel", page_icon=":robot_face:", layout="wide") 

#subprocess.run(["choco", "upgrade", "all"])
#subprocess.run(["choco", "install", "ghostscript"])


#subprocess.run(["apt-get", "update"])
#subprocess.run(["apt-get", "install", "-y", "ghostscript"])

#@st.cache_data
def gh():
    proc = subprocess.Popen('apt-get install -y ghostscript', shell=True, stdin=None, stdout=open(os.devnull,"wb"), stderr=STDOUT, executable="/bin/bash")
    proc.wait()
gh()

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

# Set page title
st.title("Akash's PDF to Excel Transformer :robot_face:")
st.write("---")

# upload the pdf
st.write('NOTE  -  This app only converts data tables from text-based PDFs and not scanned documents.')

with st.container():
    st.write('##')
    left_column, right_column = st.columns((1, 1))
    with left_column:
        input_pdf = st.file_uploader(label="Upload a PDF table file to convert to Excel", type='pdf')
    with right_column:
        st.empty()

st.write("---")

# enter page number
with st.container():
    left_column, right_column = st.columns((1, 1))
    with left_column:
        st.markdown("### Fine Tuning")
        page_number = st.text_input(""" From the PDF file, enter the page number that you want converted to Excel, for e.g., 3 
                                    """, value=1)
    with right_column:
        st.empty()

#PDF conversion
if input_pdf is not None:
    with open("input.pdf", "wb") as f:
        base64_pdf = base64.b64encode(input_pdf.read()).decode('utf-8')
        f.write(base64.b64decode(base64_pdf))
    
    table = cam.read_pdf("input.pdf", pages=page_number, flavor='lattice')

    st.write(table)

    if len(table) > 0:
        # select table to convert to Excel
        with st.container():
            left_column, right_column = st.columns((1, 1))
            with left_column:
                option = st.selectbox(label="Select the table from above selected page that you want converted to Excel", options=range(len(table)))
            with right_column:
                st.empty()

        output_table = table[option].df

        st.write("---")
        st.markdown('### Table Preview')

        # display the selected table without index column and row
        st.table(output_table.style.hide_index()) 
        
        # Convert df into Excel, CSV
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        output_table.to_excel(writer, sheet_name='Sheet1', index=False, header=False) # remove index column
        writer.save()
        output.seek(0)

        # Download
        st.write("---")
        st.write('##')
        st.download_button(
            label="Download Selected Table from PDF File",
            data=output.getvalue(),
            file_name=f"Table {option} from PDF file.xlsx"
        )
    else:
        st.write('##')
        st.write('##')
        st.markdown('### No table found on uploaded PDF file')
