"""
main.py

Displays a usage Graph for WhatPulse Applications (locally)

Author:
Nilusink
"""
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import platform
import sqlite3
import os

# selected applications
APPLICATIONS: list[str | tuple[str, str]] = [
    "pycharm",
    "Mindustry",
    ("code", "VS-Code"),
    "Discord",
    "spotify",
    ("DesktopEditors", "OnlyOffice Desktop"),
    "firefox",
]


# database connection
if platform.system() == "Linux":
    db_path = f"{os.getenv('HOME')}/.local/share/whatpulse.db"
    APPLICATIONS.extend([
        ("rawtherapee", "RawTherapee"),
        "joplin",
        ("googleearth", "Google Earth (pro)"),
        ("PacketTracer", "Packet Tracer"),
        "minecraft",
    ])

elif platform.system() == "Windows":
    db_path = fr"{os.getenv('LOCALAPPDATA')}\WhatPulse\whatpulse.db"
    APPLICATIONS.extend([
        ("dcs", "DCS"),
        ("cities", "Cities Skylines"),
        ("GTA5", "GTA V"),
        ("neonabyss", "NeonAbyss"),
    ])

elif platform.system() == "Darwin":   # macos
    db_path = "~/Library/Application Support/WhatPulse/"

else:
    raise RuntimeError("Unsupported platform")


# create database connection
conn = sqlite3.connect(db_path)


# Plot data
plt.figure(figsize=(10, 5))


# graph each application
total_times = []
for application in APPLICATIONS:
    # check for given name
    if isinstance(application, tuple):
        application, name = application

    else:
        name = application.capitalize()

    # load data into Pandas
    query = (
        f"SELECT day, hour, seconds_active FROM "
        f"application_active_hour WHERE path LIKE '%{application}%';"
    )
    df = pd.read_sql_query(query, conn)

    # Convert date column to datetime
    df['day'] = pd.to_datetime(df['day'])
    df['datetime'] = pd.to_datetime(
        df['day'].astype(str) + ' ' + df['hour'].astype(str)
    )

    # convert column to cumulative hours
    df['hours_active'] = df['seconds_active'] / 3600
    df['total_hours'] = df['hours_active'].cumsum()

    # get total hours (last entry)
    total_hours = df['total_hours'].iat[-1]
    total_times.append(total_hours)

    # add "now" with last total_hours
    df = pd.concat([
        df,
        pd.DataFrame([{
            "datetime": datetime.now(),
            "total_hours": total_hours
        }])
    ], ignore_index=True)

    # plot application
    if total_hours > 1:
        total_time = f"({total_hours:.1f} Hours)"

    else:
        total_time = f"({total_hours*60:.0f} Minutes)"

    plt.plot(
        df['datetime'],
        df['total_hours'],
        linestyle='-',
        label=f"{name} {total_time}"
    )


# close database connection
conn.close()


# Labels and title
plt.xlabel("Date")
plt.ylabel("Usage Time (hour)")
plt.title("Application Usage Over Time")

# Get handles and labels
handles, labels = plt.gca().get_legend_handles_labels()

# Sort labels and handles together
sorted_handles_labels = sorted(
    zip(labels, handles),
    key=lambda x: total_times[labels.index(x[0])],
    reverse=True
)
sorted_labels, sorted_handles = zip(*sorted_handles_labels)

# Apply sorted legend
plt.legend(sorted_handles, sorted_labels)

plt.grid()
plt.show()
