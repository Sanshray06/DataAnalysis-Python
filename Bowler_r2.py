#IMPORTING PANDAS LIBRARY
import pandas as pd

#LOADING EXCEL FILES IN DATASETS
data = pd.read_excel(r"C:\Allen\Chemistry\AMEX_ROUND2\Bowler2.xlsx")

# NOW CALCULATING POINTS ACCORDING TO QUESTION USING VARIOUS FUNCTIONS
def economy_points(eco):
    if eco <= 3:
        return 50
    elif 3 < eco <= 5:
        return 40
    elif 5 < eco <= 7:
        return 30
    else:
        return 0
def avg_points(eco):
    if eco <= 20:
        return 30
    elif 20< eco <= 30:
        return 20
    elif 30 < eco <= 40:
        return 10
    else:
        return 0
def strike_points(eco):
    if eco <= 15:
        return 30
    elif 15< eco <= 19:
        return 20
    elif 19 < eco <= 24:
        return 10
    else:
        return 0


def checkwickets(eco):
    if eco >=4:
        return 30
    elif 2<= eco <= 3:
        return 20
    elif  eco ==1:
        return 10
    else:
        return 0


def checkCon(eco):
    
    if 0.7<=eco <=1:
        return 30
    elif 0.3<= eco <0.7:
        return 20
    elif  0.1 <= eco < 0.3:
        return 10
    else:
        return 0


def wickets(wic):
    if wic>=4:
        return 1
    else:
        return 0



#CALUCATING TOTAL WICKETS AND FURTHER MERGING IT INTO THE DATAFRAME

total_wickets = data.groupby('bowler')['wicket_count'].sum().reset_index()
total_wickets.rename(columns={'wicket_count': 'total_wicket_count'}, inplace=True)
data = data.merge(total_wickets, on='bowler', how='left')

#CALCULATING TOTAL BALL BOWLED BY EACH PLAYER
total_balls_bowled = data.groupby('bowler')['balls_bowled'].sum().reset_index()
total_balls_bowled.rename(columns={'balls_bowled': 'total_balls_bowled'}, inplace=True)
data = data.merge(total_balls_bowled, on='bowler', how='left')

#CALCULATING THE STRIKE RATE OF EACH PALYER BY DIVIDING THE ROTAL BALL WITH TOTAL BALL BOWLED 
data['strike_rate'] = data['total_balls_bowled']/data['total_wicket_count']
data["strike_rate_Points"] = data["strike_rate"].apply(strike_points)


#CALCULATING THE 4 WICKETS TAKEN BY EACH PLAYER BY GIVING 1 FOR YES AND 0 FOR NO IN THE ABOVE FUNCTION
data["4_wickets"] = data['wicket_count'].apply(wickets)
#SUMMING THEM UP PLAYERWISE
total_4_haul = data.groupby('bowler')['4_wickets'].sum().reset_index()
total_4_haul.rename(columns={'4_wickets': 'total_4_haul'}, inplace=True)
#MERGING IT
data = data.merge(total_4_haul, on='bowler', how='left')

#FURTHER APPLYING POINTS FUNCTIONS 
data["total_4"] = data["total_4_haul"].apply(checkwickets)


# FURTHER CHECKED IN BETWEEN ABOUT MY PROGRESS AS WELL 
df_top_bowler = data.sort_values(by='final_Score', ascending=False).head(10)[['bowler', 'bowler_id']]


print("Top 10 Bowlers based on Weighted Score:")
for index, row in df_top_bowler.iterrows():
    print(f"Bowler Name: {row['bowler']}, Bowler ID: {row['bowler_id']}")



#THIS IS THE FUNCTION FOR THE RECENCY 
def latest_10_matches_avg(runs):
    return runs.rolling(window=10, min_periods=1).mean()

#TAKING THE LAST 10 MATCHES
data['latest_10_avg'] = data.groupby('bowler')['runs'].transform(latest_10_matches_avg)

data['latest_10_points'] = data['latest_10_avg'].apply(avg_points)

#FURTHER CHECK MY PROGRESS
data["recency_Score"] = data["total_4"] + data["strike_rate_Points"] + data["avgPoints"] + data["ecoPoints"] + data['latest_10_points']

#FINDIND ECONOMY
data['final_economy'] = (data['total_runs']/data['total_balls'])*6







def consistency_factor(group):
    runs_std = group['runs'].std()  # STANDARD DEVIATION FOR RUNS
    wickets_std = group['wicket_count'].std()  # STANDARD DEVIATION FOR WICKETS
    eco_std = group['final_economy'].std()  # STANDARD DEVIATION FOR ECONOMY

    # COMBINING ALL OF THEM AND DIVIDED BY 1 TO FIND CONSISTENCY
    consistency = 1 / (runs_std + wickets_std + eco_std)  
    return pd.Series({'consistency_fac12': consistency})



# APPLYING THE ABOVE FUNCTION
consistency_scores = data.groupby('bowler', group_keys=False).apply(consistency_factor).reset_index()

# MERGING IT
data = data.merge(consistency_scores, on='bowler', how='left')

# APPLYING THE POINTS FUNCTION
data['consistency_points'] = data['consistency_fac12'].apply(checkCon)



#FINDING TOTAL RUNS BOWLERS GOT 
total_runs = data.groupby('bowler')['runs'].sum().reset_index()
total_runs.rename(columns={'runs': 'total_runs'}, inplace=True)
#MERGING
data = data.merge(total_runs, on='bowler', how='left')


#FINDING TOTAL BALLS
total_balls = data.groupby('bowler')['balls_bowled'].sum().reset_index()
total_balls.rename(columns={'balls_bowled': 'total_balls'}, inplace=True)

data = data.merge(total_balls, on='bowler', how='left')




#FIND THE AVERAGE BY TOTAL RUNS OVER TOTAL WICKETS 
data['new_avg'] = data['total_runs']/data['total_wicket_count']
data['new_avg_points'] = data['new_avg'].apply(avg_points)
data["final_eco_score"] = data["final_economy"].apply(economy_points)


# FINALLY ADDING FOR TOTAL POINTS
data["final_Score12"] = data["total_4"] + data["strike_rate_Points"] + data["new_avg_points"] + data["final_eco_score"]

#GIVING WEIGHTAGE TO EVERY FACTOR DEPENDING UPON THEIR IMPORTANCE THAT I THOUGHT
weight_total_points =0.5
weight_consistency = 0.25
weight_recency = 0.25

# CALCULATE WEIGHTED SCORE
data['WeightedScore'] = (
    weight_total_points * data['final_Score12'] + 
    weight_consistency * data['consistency_points'] + 
    weight_recency * data['recency_Score']
)

#FOR MERGING PURPOSE 
data['ID'] = data['bowler_id']

#PUTTING THE REFINED DATA IN THE EXCEL SHEET
data.to_excel(r"C:\Allen\Chemistry\AMEX_ROUND2\Bowler2.xlsx", index=False)


print("The updated DataFrame has been saved to the Excel file.")