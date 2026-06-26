import streamlit as st
import os
import shutil


from modules.inventory_parser import extract_inventory
from modules.matcher import run_matching
from modules.pdf_generator import create_worker_pdf



BASE_PATH = os.getcwd()


st.set_page_config(
    page_title="Dyeing AI System",
    layout="wide"
)


st.title("🧵 Dyeing AI Color Management System")


st.write(
"""
Upload today's Inventory PDF.
System automatically checks Design colors,
finds available colors,
uses alternatives,
and generates worker instruction PDF.
"""
)



inventory_upload = st.file_uploader(
    "Upload Inventory PDF",
    type=["pdf"]
)



if inventory_upload:


    inventory_path = (
        BASE_PATH+
        "/input/inventory/Inventory.pdf"
    )


    with open(inventory_path,"wb") as f:
        f.write(
            inventory_upload.getbuffer()
        )


    st.success(
        "Inventory Uploaded Successfully"
    )



    if st.button(
        "Generate Worker PDF"
    ):


        with st.spinner(
            "Processing..."
        ):


            # Step 1
            inventory_df = extract_inventory(
                inventory_path
            )


            inventory_df.to_excel(
                BASE_PATH+
                "/database/inventory.xlsx",
                index=False
            )



            # Step 2
            final_df = run_matching()



            final_df.to_excel(
                BASE_PATH+
                "/output/Final_Color_Report.xlsx",
                index=False
            )



            # Step 3 PDF

            pdf_path=create_worker_pdf(
                final_df
            )


        st.success(
            "Completed Successfully"
        )


        st.download_button(
            label="Download Worker PDF",
            data=open(
                pdf_path,
                "rb"
            ),
            file_name=
            "Worker_Color_Instructions.pdf"
        )