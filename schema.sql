CREATE TABLE users(
    "id" INTEGER NOT NULL, 
    "username" TEXT NOT NULL,
    "user_id" TEXT UNIQUE NOT NULL,
    "hash" TEXT NOT NULL,
    "department" TEXT,
    "role" TEXT NOT NULL CHECK("role" IN ('employee', 'manager')),
    PRIMARY KEY("id")
);

CREATE TABLE availabilities(
    "user_id" INTEGER,
    "date" TEXT NOT NULL,  -- 'YYYY-MM-DD'
    "starting_time" TEXT NOT NULL, 
    "ending_time" TEXT NOT NULL,
    PRIMARY KEY("user_id", "date", "starting_time", "ending_time"),
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);

CREATE TABLE shifts(
    "id" INTEGER UNIQUE,
    "worker_id" INTEGER,
    "date" TEXT NOT NULL, -- 'YYYY-MM-DD'
    "starting_time" TEXT NOT NULL,
    "ending_time" TEXT NOT NULL,
    PRIMARY KEY("date", "starting_time", "ending_time"),
    FOREIGN KEY("worker_id") REFERENCES "users"("id") ON DELETE CASCADE
);


CREATE TABLE swaps(
    "id" INTEGER,
    "timestamp" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "status" TEXT CHECK("status" IN ('pending', 'approved', 'denied')),
    "shift_id" INTEGER NOT NULL,
    "requester_id" INTEGER NOT NULL,
    "responder_id" INTEGER,
    PRIMARY KEY("id"),
    FOREIGN KEY("shift_id") REFERENCES "shifts"("id") ON DELETE CASCADE,
    FOREIGN KEY("requester_id") REFERENCES "users"("id") ON DELETE CASCADE ,
   FOREIGN KEY("responder_id") REFERENCES "users"("id") ON DELETE CASCADE
); 



