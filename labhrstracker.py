import pandas as pd

#this function calculates the attendance for each student in the csv and the hours for every day lopgged. The function also notes if a student missed clocking in/out.
# under each student, there will be a like saying Total elapsed time on YYYY-MM-DD: 0 days HH:MM:SS
def calculate_elapsed_time(df):
    # Convert 'Timestamp' column to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%m/%d/%Y %H:%M:%S')

    # Standardize name formatting
    df['Your name'] = df['Your name'].str.strip().str.title()

    results = {}
    for name, group in df.groupby('Your name'):
        if len(group) == 1:
            results[name] = f"{name} missed checking in or out on {group.iloc[0]['Timestamp'].date()}\n"
        else:
            daily_results = ""
            # Get the first and last rows for each day
            daily_groups = group.groupby(group['Timestamp'].dt.date)
            for date, daily_group in daily_groups:
                if len(daily_group) == 1:
                    daily_results += f"{name} missed checking in or out on {date}\n"
                else:
                    # Calculate elapsed time for each day
                    elapsed_time = daily_group.iloc[-1]['Timestamp'] - daily_group.iloc[0]['Timestamp']
                    daily_results += f"Total elapsed time on {date}: {elapsed_time}\n"
            results[name] = daily_results

    return results

if __name__ == "__main__":
    try:
        df = pd.read_csv('sp24_attendance.csv') #change this file name to whatever the csv name is, IMPORTANT: make sure that the csv is in the same file path as this .py file!!!
        elapsed_times = calculate_elapsed_time(df)
        for name, elapsed_time in elapsed_times.items():
            print(f"{name}:\n{elapsed_time}")
    except Exception as e:
        print(f"An error occurred: {e}")
