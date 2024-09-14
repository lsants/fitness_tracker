import os
import pandas as pd
import matplotlib.pyplot as plt
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = f"{script_dir}/Musculação/"
workout_data_path = f"{data_dir}/workout_data.csv"

# ------------- Load data -----------
df = pd.read_csv(workout_data_path)

# ------------ Replace bodyweight with numerical value ----------
bodyweight = 160
f = lambda x: bodyweight if x == 'bodyweight' else float(x)
df['weight'] = df['weight'].apply(f)
df.rename(columns={'weight':'weight_lbs'}, inplace=True)

# ---------- Get total muscle work volume ------------
df['volume'] = df['sets']*df['reps']*df['weight_lbs']

# ---------- Plot work by group -------------
d = df.groupby('group')['volume'].sum()
plt.pie(d, labels=d.index, autopct='%1.1f%%')
plt.show()

print(df)