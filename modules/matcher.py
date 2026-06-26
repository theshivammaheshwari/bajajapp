import pandas as pd
import os


BASE_PATH = os.getcwd()



def load_databases():

    inventory_path = os.path.join(
        BASE_PATH,
        "database",
        "inventory.xlsx"
    )


    design_path = os.path.join(
        BASE_PATH,
        "database",
        "design.xlsx"
    )


    alternative_path = os.path.join(
        BASE_PATH,
        "database",
        "alternative.xlsx"
    )


    inventory_df = pd.read_excel(
        inventory_path
    )


    design_df = pd.read_excel(
        design_path
    )


    alternative_df = pd.read_excel(
        alternative_path
    )


    return (
        inventory_df,
        design_df,
        alternative_df
    )





def create_inventory_dict(inventory_df):

    """
    Inventory ko dictionary mein convert karega

    Example:

    {
       280:20,
       381:5
    }

    """

    inventory_dict={}


    for _,row in inventory_df.iterrows():


        color=int(
            row["Color_No"]
        )


        qty=int(
            row["Quantity"]
        )


        inventory_dict[color]=qty


    return inventory_dict






def find_final_color(
        required_color,
        inventory_dict,
        alternative_df
):


    # STEP 1
    # Direct color check


    if required_color in inventory_dict:


        if inventory_dict[required_color] > 0:


            return {
                "status":
                "AVAILABLE",

                "final_color":
                required_color
            }




    # STEP 2
    # Alternative check


    alt_row = alternative_df[
        alternative_df["Required_Color"]
        ==
        required_color
    ]



    if len(alt_row) > 0:


        alt_row = alt_row.iloc[0]


        alternative_columns=[

            "Alternative_1",
            "Alternative_2",
            "Alternative_3",
            "Alternative_4",
            "Alternative_5"

        ]



        for col in alternative_columns:


            if col in alt_row.index:


                alt_color=alt_row[col]


                if pd.isna(alt_color):
                    continue



                alt_color=int(
                    alt_color
                )


                if alt_color in inventory_dict:


                    if inventory_dict[alt_color] > 0:


                        return {

                            "status":
                            "ALTERNATIVE_USED",

                            "final_color":
                            alt_color
                        }




    # STEP 3
    # Nothing found


    return {

        "status":
        "MISSING",

        "final_color":
        None
    }







def run_matching():


    inventory_df,design_df,alternative_df = load_databases()



    inventory_dict=create_inventory_dict(
        inventory_df
    )



    result=[]



    for _,row in design_df.iterrows():


        required_color=int(
            row["Required_Color"]
        )


        result_data=find_final_color(

            required_color,

            inventory_dict,

            alternative_df

        )


        result.append({

            "Design":
            row["Design"],


            "Row":
            row["Row"],


            "Column":
            row["Column"],


            "Required_Color":
            required_color,


            "Status":
            result_data["status"],


            "Final_Color":
            result_data["final_color"]

        })



    return pd.DataFrame(result)
