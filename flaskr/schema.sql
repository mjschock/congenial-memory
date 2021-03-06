DROP TABLE IF EXISTS experiment;

CREATE TABLE experiment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  result TEXT NOT NULL,
  test_data TEXT NOT NULL,
  train_data TEXT NOT NULL
);