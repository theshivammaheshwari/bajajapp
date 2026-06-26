import pdfplumber
import re
import pandas as pd



def extract_inventory(pdf_path):


    data=[]


    with pdfplumber.open(pdf_path) as pdf:


        text=""


        for page in pdf.pages:

            text += page.extract_text()+"\n"



    lines=text.split("\n")



    for line in lines:


        match=re.search(
            r'MTR[- ]?(\d+).*?(\d+)\s*PCS',
            line
        )


        if match:


            color=int(
                match.group(1)
            )


            qty=int(
                match.group(2)
            )


            data.append({

                "Color_No":color,

                "Quantity":qty

            })



    return pd.DataFrame(data)