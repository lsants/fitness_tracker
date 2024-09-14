import os
import glob
import pandas as pd
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = f"{script_dir}/Musculação/"
workout_data_path = f"{data_dir}/workout_data.csv"

def get_last_timestamp(path):
    end = -len('.json')
    start = end - len('DDMMYYYY')
    file_list = glob.glob(path + '*.json')
    last_file_path = ''
    for file in file_list:
        if file[:end] > last_file_path:
            last_timestamp = file[start:end]
    return last_timestamp

def process(df):
    df_exercises = pd.json_normalize(df['exercises'])
    df =  pd.concat([df.drop(columns=['exercises']), df_exercises], axis=1)
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df

# ------------------ Get last workout file --------------
last_timestamp = get_last_timestamp(data_dir)
new_file_name = data_dir + last_timestamp + '.json'
last_timestamp = pd.to_datetime(last_timestamp, format='%d%m%Y').date()
new_data = process(pd.read_json(new_file_name))
cols = ['date', 'workout', 'name', 'group', 'sets', 'reps', 'weight']

# -------------------- Update data ------------------------
if __name__ == '__main__':
    try:
        data = pd.read_csv(workout_data_path)
        data['date'] = pd.to_datetime(data['date'], errors='coerce').dt.date
    except FileNotFoundError:
        data = pd.DataFrame(columns=cols)

    if last_timestamp not in data['date'].values:
        data = pd.concat([data, new_data], ignore_index=True)
        data.to_csv(workout_data_path, index=False, date_format='%Y-%m-%d')