from reportlab.platypus import *
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

import os



BASE_PATH=os.getcwd()



def create_design_table(design_df):


    max_row=int(
        design_df["Row"].max()
    )

    max_col=int(
        design_df["Column"].max()
    )


    table_data=[]



    for r in range(1,max_row+1):


        row=[]


        for c in range(1,max_col+1):


            cell=design_df[
                (design_df["Row"]==r)
                &
                (design_df["Column"]==c)
            ]


            if len(cell):


                status=cell.iloc[0]["Status"]

                color=cell.iloc[0]["Final_Color"]



                if status=="MISSING":

                    value="NA"


                elif status=="ALTERNATIVE_USED":

                    value=str(int(color))+"*"


                else:

                    value=str(int(color))


            else:

                value=""


            row.append(value)


        table_data.append(row)



    table=Table(
        table_data,
        colWidths=0.45*inch,
        rowHeights=0.35*inch
    )



    table.setStyle(
        TableStyle([

            (
            "GRID",
            (0,0),
            (-1,-1),
            0.5,
            colors.black
            ),


            (
            "ALIGN",
            (0,0),
            (-1,-1),
            "CENTER"
            ),


            (
            "VALIGN",
            (0,0),
            (-1,-1),
            "MIDDLE"
            )


        ])
    )


    return table







def create_worker_pdf(final_df):



    output_path=os.path.join(

        BASE_PATH,

        "output",

        "Worker_Color_Instructions.pdf"

    )



    doc=SimpleDocTemplate(

        output_path,

        pagesize=A4,

        rightMargin=30,

        leftMargin=30,

        topMargin=30,

        bottomMargin=30

    )



    styles=getSampleStyleSheet()


    elements=[]



    designs=list(
        final_df["Design"].unique()
    )


    count=0



    page_tables=[]



    for design in designs:


        design_data=final_df[
            final_df["Design"]==design
        ]



        heading=Paragraph(

            design,

            styles["Heading3"]

        )



        table=create_design_table(
            design_data
        )



        block=[

            heading,

            table,

            Spacer(1,20)

        ]



        page_tables.extend(block)



        count+=1



        # 4 design per page


        if count%4==0:


            elements.extend(
                page_tables
            )


            elements.append(
                PageBreak()
            )


            page_tables=[]



    # remaining designs


    if page_tables:


        elements.extend(
            page_tables
        )



    doc.build(elements)



    return output_path