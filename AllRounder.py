
#IMPORTING PANDAS

import pandas as pd



excel_file_path = r"C:\Allen\Chemistry\AMEX_ROUND2\allRounder.xlsx"
data = pd.read_excel(excel_file_path)

#FINDING TOTAL POINTS
data['allRound_points'] = data['TotalPoints'] + data['final_Score12']


#NORMALIZING BOTH WEIGHTED SCORES
data['x'] = (data['WeightedScore_x']/55)*100
data['y'] = (data['WeightedScore_y']/100)*100
data['allRound_points_check'] = data['TotalPoints'] + data['final_Score12'] + data['x'] +  data['y']


data.to_excel(excel_file_path, index=False)

print("The updated DataFrame has been saved to the Excel file.")