from yoyo import step

step(
    apply="""
        CREATE TABLE sets (
            set_id INTEGER NOT NULL PRIMARY KEY,
            code   TEXT    NOT NULL,
            name   TEXT    NOT NULL,
            CONSTRAINT u_code UNIQUE (code)
        );""",
    rollback="DROP TABLE sets;"
)
