CREATE TABLE items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT UNIQUE NOT NULL,      -- np. "looting-mk2"
  name TEXT NOT NULL,
  description TEXT,
  rarity TEXT NOT NULL,
  value INTEGER NOT NULL,
  weight REAL NOT NULL,
  category TEXT NOT NULL,                      -- as per in game category
  stack_size INTEGER DEFAULT 1,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);