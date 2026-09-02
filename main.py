import pandas as pd

# Load the CSV file
data = pd.read_csv("weather_data.csv")

# Display the data
print(data)
average_temperature = data["temperature"].mean()

print("Average Temperature:", average_temperature)
highest_temperature = data["temperature"].max()
lowest_temperature = data["temperature"].min()

print("Highest Temperature:", highest_temperature)
print("Lowest Temperature:", lowest_temperature)
average_rainfall = data["rainfall"].mean()
total_rainfall = data["rainfall"].sum()

print("Average Rainfall:", average_rainfall)
print("Total Rainfall:", total_rainfall)
import matplotlib.pyplot as plt

plt.plot(data["date"], data["temperature"])

plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Over Time")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
data["date"] = pd.to_datetime(data["date"])
data["month"] = data["date"].dt.month
monthly_temperature = data.groupby("month")["temperature"].mean()

print(monthly_temperature)