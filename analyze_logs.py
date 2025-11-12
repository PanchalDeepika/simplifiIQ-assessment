import pandas as pd
from datetime import datetime

sample_data = [
    ["aisha", "data_cleanup", "2025-10-18 09:10:12", 35],
    ["aisha", "report_generation", "2025-10-18 10:00:00", 50],
    ["raj", "data_cleanup", "2025-10-18 09:30:00", 25],
    ["raj", "testing", "2025-10-18 11:00:00", 40],
    ["meera", "data_entry", "2025-10-18 09:00:00", 60],
    ["meera", "data_cleanup", "2025-10-18 11:15:00", -10],  # invalid negative
    ["arun", "report_generation", "2025-10-18 10:20:00", None],  # missing
    ["arun", "testing", "invalid_date", 45],  # bad timestamp
    ["neha", "data_entry", "2025-10-18 08:55:00", 30],
]
columns = ["user", "task_type", "start", "duration_min"]

df_sample = pd.DataFrame(sample_data, columns=columns)
df_sample.to_csv("task_logs.csv", index=False)

print("Sample CSV 'task_logs.csv' created.\n")

# --- Step 2: Read CSV ---
df = pd.read_csv("task_logs.csv")

# --- Step 3: Data Cleaning ---
def is_valid_timestamp(x):
    try:
        datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
        return True
    except Exception:
        return False

# Filter invalid timestamps
df = df[df["start"].apply(is_valid_timestamp)]

# Convert columns
df["duration_min"] = pd.to_numeric(df["duration_min"], errors="coerce")

# Drop rows with missing or negative durations
df = df.dropna(subset=["duration_min"])
df = df[df["duration_min"] >= 0]

# --- Step 4: Aggregations ---
# Total time spent per user
time_per_user = df.groupby("user")["duration_min"].sum().sort_values(ascending=False)

# Total time per task type
time_per_task = df.groupby("task_type")["duration_min"].sum().sort_values(ascending=False)

# Top 3 task types
top3_tasks = time_per_task.head(3)

# --- Step 5: Output Summary ---
print("===== SUMMARY REPORT =====")
print("\n-- Total Time per User (minutes) --")
print(time_per_user)

print("\n-- Total Time per Task Type (minutes) --")
print(time_per_task)

print("\n-- Top 3 Task Types by Total Time --")
print(top3_tasks)

# --- Step 6: Save to CSV ---
summary_df = pd.DataFrame({
    "Total_Time_per_User": time_per_user,
}).reset_index()

summary_df2 = pd.DataFrame({
    "Task_Type": time_per_task.index,
    "Total_Time_Min": time_per_task.values
})

summary_df.to_csv("user_summary.csv", index=False)
summary_df2.to_csv("task_summary.csv", index=False)

print("\nReports saved as 'user_summary.csv' and 'task_summary.csv'.")
