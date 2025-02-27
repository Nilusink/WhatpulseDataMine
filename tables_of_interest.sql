CREATE TABLE application_uptime (
        "last_active" DATETIME NOT NULL,
        "last_used" DATETIME,
        "time" INTEGER NOT NULL DEFAULT 0,
        "path" VARCHAR NOT NULL,
        "profile_id" INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE application_active_hour (
        "day" DATE NOT NULL,
        "hour" INTEGER NOT NULL,
        "seconds_active" INTEGER NOT NULL DEFAULT 0,
        "path" VARCHAR NOT NULL,
        "profile_id" INTEGER NOT NULL DEFAULT 0
);
CREATE UNIQUE INDEX application_active_hour_day_hour_path ON application_active_hour ( day, hour, path, profile_id );