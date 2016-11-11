from yoyo import step

step(
    apply="""
        CREATE TABLE users (
            user_id       INTEGER NOT NULL PRIMARY KEY,
            username      TEXT NOT NULL,
            password_salt BLOB NOT NULL,
            password_hash BLOB NOT NULL,
            CONSTRAINT u_username UNIQUE (username)
        );""",
    rollback="DROP TABLE users;"
)
