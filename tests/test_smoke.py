"""Smoke tests: these should always be green. If one of them is red, something basic is broken."""

import os

from streamlit.testing.v1 import AppTest

import db
import seed
from conftest import REPO_DIR, SEED_DIR

APP_PATH = os.path.join(REPO_DIR, "app.py")


def test_app_imports_and_renders(fresh_data):
    """The home screen and a group page both render without any exception."""
    app = AppTest.from_file(APP_PATH, default_timeout=60).run()
    assert not app.exception
    assert app.title[0].value == "SplitIt"
    app.button[0].click().run()
    assert not app.exception
    assert len(app.table) == 1


def test_every_table_loads(fresh_data):
    """Each CSV opens, has rows, and has exactly the columns db.py expects."""
    for table_name in ["groups", "members", "expenses"]:
        rows = db.load_table(table_name)
        assert len(rows) > 0
        assert list(rows[0].keys()) == db.COLUMNS[table_name]


def test_append_row_adds_one_row(fresh_data):
    """append_row writes a new line at the end of the file and next_id moves on."""
    before = len(db.load_table("members"))
    new_id = db.next_id("members")
    db.append_row("members", {"id": new_id, "group_id": "1", "name": "Teste"})
    rows = db.load_table("members")
    assert len(rows) == before + 1
    assert rows[-1]["name"] == "Teste"
    assert db.next_id("members") == new_id + 1


def test_seed_restores_the_data(tmp_path):
    """After changing a CSV, seed.reset_data puts back the pristine copy."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "members.csv").write_text("id,group_id,name\n99,1,Intruso\n", encoding="utf-8")
    copied = seed.reset_data(SEED_DIR, str(data_dir))
    assert copied == ["expenses.csv", "groups.csv", "members.csv"]
    for file_name in copied:
        with open(os.path.join(SEED_DIR, file_name), encoding="utf-8") as pristine:
            assert (data_dir / file_name).read_text(encoding="utf-8") == pristine.read()
