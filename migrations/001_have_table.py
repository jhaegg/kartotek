from yoyo import step

step(
    apply="""
        CREATE TABLE have (
            mvid        INTEGER NOT NULL PRIMARY KEY,
            num_regular INTEGER NOT NULL DEFAULT 0,
            num_foil    INTEGER NOT NULL DEFAULT 0
        );""",
    rollback="DROP TABLE have;"
)
