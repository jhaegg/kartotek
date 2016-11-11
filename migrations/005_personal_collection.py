from yoyo import step

step(
    apply="ALTER TABLE have ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1 REFERENCES users (user_id);",
    rollback="ALTER TABLE have DROP COLUMN user_id;"
)
