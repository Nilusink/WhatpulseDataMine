"""
main.py

Displays a usage Graph for WhatPulse Applications (locally)

Author:
Nilusink
"""
import matplotlib.pyplot as plt
import pandas as pd
import platform
import sqlite3
import os

# selected applications
APPLICATIONS: list[str] = [
    "pycharm",
    "Mindustry",
    "code",
    "Discord",
    "spotify",
    "DesktopEditors",
    "minecraft",
    "firefox"
]


# database connection
if platform.system() == "Linux":
    db_path = f"{os.getenv('HOME')}/.local/share/whatpulse.db"
    APPLICATIONS.extend([
        "rawtherapee",
        "joplin",
        "googleearth",
        "PacketTracer",
    ])

elif platform.system() == "Windows":
    db_path = fr"{os.getenv('LOCALAPPDATA')}\WhatPulse\whatpulse.db"
    APPLICATIONS.extend([
        "dcs",
        "cities",
        "GTA5",
        "neonabyss"
    ])

elif platform.system() == "Darwin":   # macos
    db_path = "~/Library/Application Support/WhatPulse/"

else:
    raise RuntimeError("Unsupported platform")

conn = sqlite3.connect(db_path)

# Plot data
plt.figure(figsize=(10, 5))

# graph each application
for application in APPLICATIONS:
    # load data into Pandas
    query = f"SELECT day, hour, seconds_active FROM application_active_hour WHERE path LIKE '%{application}%';"  # " WHERE path like '%firefox%'"
    df = pd.read_sql_query(query, conn)

    # Convert date column to datetime
    df['day'] = pd.to_datetime(df['day'])
    df['datetime'] = pd.to_datetime(df['day'].astype(str) + ' ' + df['hour'].astype(str))

    # convert column to cumulative hours
    df['hours_active'] = df['seconds_active'] / 3600
    df['total_hours'] = df['hours_active'].cumsum()

    # plot application
    plt.plot(
        df['datetime'],
        df['total_hours'],
        linestyle='-',
        label=f"{application.capitalize()} ({df['total_hours']} Hours)"
    )

conn.close()

# Labels and title
plt.xlabel("Date")
plt.ylabel("Usage Time (hour)")
plt.title("Application Usage Over Time")
plt.legend()
plt.grid()
plt.show()
