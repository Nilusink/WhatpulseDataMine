"""
main.py

Displays a usage Graph for WhatPulse Applications (locally)

Author:
Nilusink
"""
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import os

# selected applications
APPLICATIONS: list[str] = [
    "pycharm",
#    "firefox",
#    "chromium",
    "Mindustry",
    "code",
#    "minecraft",
    "rawtherapee",
    "joplin",
#    "balena-etcher",
    "googleearth",
    "PacketTracer",
    "Discord",
    "spotify",
    "DesktopEditors"
]


# database connection
conn = sqlite3.connect(f"{os.getenv('HOME')}/.local/share/whatpulse.db")

# Plot data
plt.figure(figsize=(10, 5))

# graph each application
for application in APPLICATIONS:
    # load data into Pandas
    query = f"SELECT day, hour, seconds_active FROM application_active_hour WHERE path LIKE '%{application}%';"  # " WHERE path like '%firefox%'"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert date column to datetime
    df['day'] = pd.to_datetime(df['day'])
    df['datetime'] = pd.to_datetime(df['day'].astype(str) + ' ' + df['hour'].astype(str))

    # convert column to cumulative hours
    df['hours_active'] = df['seconds_active'] / 3600
    df['total_hours'] = df['hours_active'].cumsum()

    # plot application
    plt.plot(df['datetime'], df['total_hours'], linestyle='-', label=application.capitalize())

# Labels and title
plt.xlabel("Date")
plt.ylabel("Usage Time (hour)")
plt.title("Application Usage Over Time")
plt.legend()
plt.grid()
plt.show()
