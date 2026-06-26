import pandas as pd
import os



BASE=os.getcwd()



def run_matching():


    inventory=pd.read_excel(
        BASE+
        "/database/inventory.xlsx"
    )


    design=pd.read_excel(
        BASE+
        "/database/design.xlsx"
    )


    alternative=pd.read_excel(
        BASE+
        "/database/alternative.xlsx"
    )



    inventory_colors=set(
        inventory["Color_No"]
    )



    result=[]



    for _,row in design.iterrows():


        required=row["Required_Color"]



        if required in inventory_colors:


            result.append({

                **row,

                "Status":
                "AVAILABLE",

                "Final_Color":
                required

            })


        else:


            found=None


            alt_row=alternative[
                alternative.Required_Color
                ==
                required
            ]



            if len(alt_row):


                for col in [
                    "Alternative_1",
                    "Alternative_2",
                    "Alternative_3",
                    "Alternative_4",
                    "Alternative_5"
                ]:


                    if col in alt_row:


                        color=alt_row.iloc[0][col]


                        if color in inventory_colors:

                            found=color

                            break



            if found:


                result.append({

                **row,

                "Status":
                "ALTERNATIVE_USED",

                "Final_Color":
                found

                })


            else:


                result.append({

                **row,

                "Status":
                "MISSING",

                "Final_Color":
                None

                })



    return pd.DataFrame(result)