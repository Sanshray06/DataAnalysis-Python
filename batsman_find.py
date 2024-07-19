import pandas as pd

# SPECIFING DATASET TO EXCEL FILE
excel_file_path = r"C:\Allen\Chemistry\AMEX_ROUND2\Batsman.xlsx"


df = pd.read_excel(excel_file_path)


#THIS WAS DONE IN BETWEEN THE PROCESS TO TRACK THE PROGRESS

#FINDING BATSMANS WITH SCORE 110 WHICH IS THE HIGHEST
filtered_df = df[df['TotalPoints'] == 110][['batsman', 'batsman_id']].drop_duplicates()

#PRINTING NAMES AND IDS OF BATSMANS WHICH HAVE TOTAL POINTS:110
for index, row in filtered_df.iterrows():
    print(f"Batsman Name: {row['batsman']}, Batsman ID: {row['batsman_id']}")