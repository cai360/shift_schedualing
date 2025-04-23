from app import db


db.execute("""
    CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    user_id TEXT UNIQUE, 
    hash TEXT NOT NULL,                        
    department TEXT,
    role TEXT CHECK (role IN ('employee', 'manager'))
    )""")

db.execute("""
    CREATE TABLE availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    employee_id INTEGER NOT NULL,       
    available_date DATE NOT NULL,       
    start_time TIME NOT NULL,           
    end_time TIME NOT NULL,            
    FOREIGN KEY(employee_id) REFERENCES users(id) ON DELETE CASCADE
)""")

db.execute("""
    CREATE TABLE schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        employee_id INTEGER,
        date NUMERIC,                
        start_time TIME,           
        end_time TIME,             
        FOREIGN KEY(employee_id) REFERENCES users(id) ON DELETE CASCADE
    )
 """)

db.execute("""
    CREATE TABLE Swap (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
        status TEXT CHECK (status IN ('pending', 'approved', 'denied')), 
        shift_id INTEGER NOT NULL,          
        requester_id INTEGER NOT NULL,       
        responder_id INTEGER,                
        FOREIGN KEY (shift_id) REFERENCES schedule(id) ON DELETE CASCADE,
        FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (responder_id) REFERENCES users(id) ON DELETE SET NULL
    )
 """)


