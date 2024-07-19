

#IMPORTING PANDAS
import pandas as pd


# FUNCTION MERGING DATA OF 2 EXCEL FILES 

#THIS IS SIMILAR TO WHAT WE DO IN SQL(JOINS)
def merge_excel_sheets(file1, file2, output_file, column):
    
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    merged_df = pd.merge(df1, df2, on=column, how='inner')

    merged_df.to_excel(output_file, index=False)
    print(f'Merged file saved as {output_file}')


#USING ABOVE FUNCTION TO MERGE THE DATA OF 2 EXCEL FILES 

merge_excel_sheets(r'C:\Allen\Chemistry\AMEX_ROUND2\batsman_id.xlsx', r'C:\Allen\Chemistry\AMEX_ROUND2\bowler_id.xlsx', r'C:\Allen\Chemistry\AMEX_ROUND2\allRounder.xlsx', 'id')
