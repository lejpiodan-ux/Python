import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file = r'/content/Waga.xlsx'
df = pd.read_excel(file)


df = df.rename(columns={'Dzień': 'Day', 'Waga': 'Weight'})

# Weight prediction for days 51-100 based on weight changes during days 0-50
df['Weight_change'] = df['Weight'].diff().round(1)
changes = df['Weight_change'].dropna()

change_statistics = changes.value_counts(normalize=True)
display(change_statistics)

# Converting data to lists
possible_changes = change_statistics.index.tolist()
probabilities = change_statistics.values.tolist()
sampled_changes = np.random.choice(possible_changes, 50, p=probabilities)

# 1. Check where day 50 ended
last_weight = df['Weight'].iloc[-1]  

# 2. Prepare empty lists for new days and predicted weights
forecast_days = np.arange(51, 101)  
forecast_weights = []

# 3. Loop simulating the next days
current_weight = last_weight
for change in sampled_changes:
    current_weight += change
    forecast_weights.append(round(current_weight, 1))

# Creating the new forecast dataframe
df_forecast = pd.DataFrame({
    'Day': forecast_days,
    'Weight': forecast_weights
})

combined_days = [df['Day'].iloc[-1]] + list(df_forecast['Day'])
combined_weights = [df['Weight'].iloc[-1]] + list(df_forecast['Weight'])

# Chart setup
plt.figure(figsize=(14, 10))

# Historical data line
plt.plot(
    df['Day'],
    df['Weight'],
    color='#01082D',
    label='Historical Data'
)

# Forecast line
plt.plot(
    combined_days,
    combined_weights,
    label="A forecast based on historical data",
    linestyle="--",
    linewidth=2,
    alpha=0.4,
    color='#266CA9'
)

# Goal and event indicators
plt.axhline(103.3, color='#006d2c', linewidth=0.75, label='Starting weight (103,3 kg)')
plt.axvline(20, color='red', linewidth=0.75, label='Added 10,000 steps every day')


plt.title(
    'Weight Trajectory After Cutting Refined Sugar and Adding 10,000 Steps Daily',
    fontsize='14',
    fontweight='bold', 
    color='#222016',
    pad=20
)

plt.xlabel(
    'Day',
    fontsize=10,
    fontweight='bold',
    color='#373737',
    labelpad=15
)

plt.ylabel(
    'Weight (kg)',
    fontsize=10,
    fontweight='bold',
    color='#373737'
)

# Annotation for Day 50 (Current State)
x_point = df["Day"].iloc[-1]
y_point = df["Weight"].iloc[-1]

plt.plot(
    [x_point, x_point],
    [y_point - 2, y_point + 2], 
    color="#222016",
    linestyle="-",
    linewidth=1.5,
)

# FIXED: Added the missing closing parenthesis at the end of plt.text
plt.text(
    x_point + 1.5,  
    y_point + 1.5,  
    f'Now\n{y_point} kg',
    fontweight="bold",
    color="#222016",
    fontsize=10,
    va="bottom"
)

# Grid and layout settings
plt.xticks(np.arange(0, 101, 5))
plt.xlim(1, 100)
plt.ylim(80, 110)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.legend()
plt.show()
