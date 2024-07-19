
#IMPORTING PANDAS LIBRARY
import pandas as pd

#LOADING EXCEL FILES IN DATASETS


excel_file = r"C:\Allen\Chemistry\AMEX_ROUND2\Batsman.xlsx"
df = pd.read_excel(excel_file)


# NOW CALCULATING POINTS ACCORDING TO QUESTION USING VARIOUS FUNCTIONS


def calculate_score(strike_rate):
    if strike_rate >= 150:
        return 50
    elif 100 <= strike_rate < 150:
        return 40
    elif 80 <= strike_rate < 100:
        return 30
    else:
        return 0

def calculate_score_avg(avg):
    if avg >= 50:
        return 30
    elif 40 <= avg < 50:
        return 20
    elif 30 <= avg < 40:
        return 10
    else:
        return 5

def calculate_score_consistency(std_dev):
    if pd.isnull(std_dev):
        return 0
    if std_dev <= 7:
        return 20
    elif 7 < std_dev <= 15:
        return 10
    elif 15 < std_dev <= 30:
        return 5
    else:
        return 0

def calculate_score_100(val1):
    if val1 >= 3:
        return 30
    elif 2 <= val1 < 3:
        return 20
    elif 1 <= val1 < 2:
        return 10
    else:
        return 0

def calculate_score_50(val2):
    if val2 >= 5:
        return 20
    elif 3 <= val2 < 5:
        return 10
    elif 1 <= val2 < 3:
        return 5
    else:
        return 0




# CREATING A NEW COLUMN AND APPLYING A FUNCTION

df['score'] = df['strike_rate'].apply(calculate_score)



# GROUPING BY BATSMANS AND TRANSFORMING USING MEAN FUNCTION

average_scores = df.groupby('batsman')['runs'].transform('mean')
df['avg'] = average_scores # MAKING A NEW COLUMN AND PUTTING THE DATA IN IT

average_scores = df.groupby('batsman')['strike_rate'].transform('mean')
df['avg_strike_rate'] = average_scores 
df['score'] = df['avg_strike_rate'].apply(calculate_score)
# USING THIS COLUMN AND APPLING THE FUNCTION FOR POINTS

df['score2'] = df['avg'].apply(calculate_score_avg)


# CHECKING THE RUNS ROW-WISE AND PUTTING 1 OR 0 ACCORDING TO OUR REQUIREMENTS

df['100s'] = df.apply(lambda row: 1 if row['runs'] >= 100 else 0, axis=1)
df['50s'] = df.apply(lambda row: 1 if 50 <= row['runs'] < 100 else 0, axis=1)



# NOW SUMMING UP OVERALL VALUES AND RENAMING IT FOR BETTER CLARITY


hundreds = df.groupby('batsman')['100s'].sum().reset_index().rename(columns={'100s': 'total_100s'})
fifties = df.groupby('batsman')['50s'].sum().reset_index().rename(columns={'50s': 'total_50s'})

# MERGING THIS STUFF TO OUR MAIN DATA

df = df.merge(hundreds, on='batsman')
df = df.merge(fifties, on='batsman')

# FROM THE DATA AND FUNCTION MAKING A NEW COLUMN 
df['score3'] = df['total_100s'].apply(calculate_score_100)
df['score4'] = df['total_50s'].apply(calculate_score_50)

# CALCULATING TOTAL POINTS
df['TotalPoints'] = df['score'] + df['score2'] + df['score3'] + df['score4']


# CALCULATING CONSISTENCY BY USING STANARD DEVIATION PARAMETER ON RUNS
#THE MORE THE VALUE THE WORSER THE CONSISTENCY
consistency = df.groupby('batsman')['runs'].std().reset_index().rename(columns={'runs': 'consistency'})


# MERGING IT...
df = df.merge(consistency, on='batsman', how='left')

# CACULATING CONSISTENCY POINTS
df['consistency_score'] = df['consistency'].apply(calculate_score_consistency)


# CALCULATNG RECENCY FACTOR
recent_matches = 20   
df['average_score_recent'] = df.groupby('batsman')['runs'].rolling(recent_matches, min_periods=1).mean().reset_index(0, drop=True)

df['Recency_score_avg'] = df['average_score_recent'].apply(calculate_score_avg)



# GIVING WEIGHTAGE TO EACH SECTION 
weight_total_points =0.5
weight_consistency = 0.25
weight_recency = 0.25

# CALCULATING WEIGHTEDSCORE
df['WeightedScore'] = (
    weight_total_points * df['TotalPoints'] + 
    weight_consistency * df['consistency_score'] + 
    weight_recency * df['Recency_score_avg']
)


df_sorted = df.sort_values(by='WeightedScore', ascending=False)

# DROPING DUPLICATES
df_unique = df_sorted.drop_duplicates(subset='batsman', keep='first')

# SELECTING TOP 20 BATSMAN
top_20_batsmen = df_unique.head(20)

print(top_20_batsmen['batsman'].tolist())


run = df.groupby('batsman')['runs'].sum().reset_index().rename(columns={'runs': 'total_runs'})

# CALCULATING TOTAL RUNS

df = df.merge(run, on='batsman')

# SAVING THE DATASET INTO OUR EXCEL FILE
df.to_excel(excel_file, index=False)

print("The updated DataFrame has been saved to the Excel file.")
