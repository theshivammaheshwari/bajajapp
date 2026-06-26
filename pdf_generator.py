from reportlab.platypus import *
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

import os



def create_worker_pdf(df):


    path=os.getcwd()+\
    "/output/Worker_Color_Instructions.pdf"



    doc=SimpleDocTemplate(
        path,
        pagesize=A4
    )



    elements=[]

    styles=getSampleStyleSheet()



    for design in df.Design.unique():


        temp=df[
            df.Design==design
        ]



        elements.append(
            Paragraph(
                design,
                styles["Heading2"]
            )
        )



        table=[]


        for r in range(
            1,
            temp.Row.max()+1
        ):


            row=[]


            for c in range(
                1,
                temp.Column.max()+1
            ):


                cell=temp[
                    (temp.Row==r)&
                    (temp.Column==c)
                ]


                if len(cell):

                    row.append(
                        str(
                        cell.iloc[0]
                        ["Final_Color"]
                        )
                    )

                else:

                    row.append("")



            table.append(row)



        t=Table(table)


        t.setStyle(
            TableStyle(
                [
                ('GRID',
                (0,0),
                (-1,-1),
                1,
                colors.black)
                ]
            )
        )


        elements.append(t)

        elements.append(PageBreak())



    doc.build(elements)


    return path