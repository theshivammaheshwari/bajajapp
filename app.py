import streamlit as st
import os
import pandas as pd
import shutil


from modules.inventory_parser import extract_inventory
from modules.matcher import run_matching
from modules.pdf_generator import create_worker_pdf



# -----------------------------
# PATH CONFIG
# -----------------------------

BASE_PATH = os.getcwd()


INVENTORY_UPLOAD_PATH = os.path.join(
    BASE_PATH,
    "input",
    "inventory",
    "Inventory.pdf"
)


INVENTORY_EXCEL_PATH = os.path.join(
    BASE_PATH,
    "database",
    "inventory.xlsx"
)


REPORT_PATH = os.path.join(
    BASE_PATH,
    "output",
    "Final_Color_Report.xlsx"
)



# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Bajaj Thread AI",
    page_icon="🧵",
    layout="wide"
)



# -----------------------------
# HEADER
# -----------------------------

st.title(
    "🧵 Bajaj Thread Color Matching AI"
)


st.write(
"""
Upload today's Inventory PDF.
System will automatically check:

✔ Available Colors  
✔ Alternative Colors  
✔ Missing Colors  

and generate Worker Instruction PDF.
"""
)



st.divider()



# -----------------------------
# FILE UPLOAD
# -----------------------------

inventory_file = st.file_uploader(
    "Upload Inventory PDF",
    type=["pdf"]
)



if inventory_file:


    # Save uploaded PDF

    with open(
        INVENTORY_UPLOAD_PATH,
        "wb"
    ) as f:

        f.write(
            inventory_file.getbuffer()
        )


    st.success(
        "Inventory PDF Uploaded"
    )



    # -----------------------------
    # PROCESS BUTTON
    # -----------------------------

    if st.button(
        "🚀 Generate Worker Instruction PDF"
    ):


        with st.spinner(
            "Processing Inventory..."
        ):


            # STEP 1
            # PDF -> Excel


            inventory_df = extract_inventory(
                INVENTORY_UPLOAD_PATH
            )


            inventory_df.to_excel(
                INVENTORY_EXCEL_PATH,
                index=False
            )



            # STEP 2
            # Matching


            final_df = run_matching()



            final_df.to_excel(
                REPORT_PATH,
                index=False
            )



            # STEP 3
            # Worker PDF


            pdf_path = create_worker_pdf(
                final_df
            )



        st.success(
            "Completed Successfully 🎉"
        )



        st.divider()



        # -----------------------------
        # SUMMARY
        # -----------------------------


        st.subheader(
            "Report Summary"
        )


        col1,col2,col3 = st.columns(3)



        with col1:

            st.metric(
                "Total Colors",
                len(final_df)
            )


        with col2:

            available=len(
                final_df[
                    final_df.Status=="AVAILABLE"
                ]
            )


            st.metric(
                "Available",
                available
            )



        with col3:


            alternative=len(
                final_df[
                    final_df.Status=="ALTERNATIVE_USED"
                ]
            )


            st.metric(
                "Alternative Used",
                alternative
            )



        missing=len(
            final_df[
                final_df.Status=="MISSING"
            ]
        )



        st.warning(
            f"Missing Colors : {missing}"
        )



        st.divider()



        # -----------------------------
        # DOWNLOAD BUTTONS
        # -----------------------------


        st.subheader(
            "Download Files"
        )


        with open(
            pdf_path,
            "rb"
        ) as file:


            st.download_button(

                label="📄 Download Worker PDF",

                data=file,

                file_name=
                "Worker_Color_Instructions.pdf",

                mime=
                "application/pdf"

            )



        with open(
            REPORT_PATH,
            "rb"
        ) as file:


            st.download_button(

                label="📊 Download Excel Report",

                data=file,

                file_name=
                "Final_Color_Report.xlsx",

                mime=
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            )