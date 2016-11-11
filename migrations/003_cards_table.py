from yoyo import step

step(
    apply="""
        CREATE TABLE cards (
            mvid    INTEGER NOT NULL,
            set_id  INTEGER NOT NULL,
            name    TEXT    NOT NULL,
            printed TEXT    NOT NULL,
            oracle  TEXT    NOT NULL,
            cost    TEXT    NOT NULL,
            cmc     INTEGER NOT NULL,
            rarity  TEXT    NOT NULL,
            FOREIGN KEY (set_id) REFERENCES sets (set_id)
        );""",
    rollback="DROP TABLE cards;"
)
