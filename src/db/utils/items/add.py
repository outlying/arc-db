#!/usr/bin/env python3
import argparse
import re
import sqlite3
import sys
from pathlib import Path

from src.db import SQLITE_DATABASE


def connect_db(db_path: str) -> sqlite3.Connection:
    db_file = Path(db_path)
    if not db_file.exists():
        print(f"ERROR: Plik bazy '{db_path}' nie istnieje.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_items_table(conn: sqlite3.Connection) -> None:
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='items';"
    )
    if cur.fetchone() is None:
        print("ERROR: W bazie nie znaleziono tabeli 'items'.", file=sys.stderr)
        sys.exit(1)


def add_item(conn: sqlite3.Connection, args: argparse.Namespace) -> None:

    assert args.name, "Name must be non-empty"
    assert args.value > 0, "Value has to be greater than zero"
    assert args.weight > 0, "Weight has to be greater than zero"
    assert args.stack_size >= 1, "Stack size has to be greater or equal one"

    name = str.strip(args.name)
    slug = re.sub(r'\s+', '-', str.lower(name))
    rarity = str.lower(str.strip(args.rarity))
    category = str.lower(str.strip(args.category))

    rarity_options = ["common", "rare"]
    assert rarity in rarity_options, f"Rarity has to be one of {rarity_options}, and it was {rarity}"

    category_options = ["misc"]
    assert category in category_options, f"Category has to be one of {category_options}, and it was {category}"

    payload = {
        "slug": name,
        "name": slug,
        "description": args.description,
        "rarity": rarity,
        "value": args.value,
        "weight": args.weight,
        "category": category,
        "stack_size": args.stack_size,
    }

    to_insert = {k: v for k, v in payload.items() if v is not None}

    if "slug" not in to_insert or "name" not in to_insert:
        print("ERROR: Pola 'slug' i 'name' są wymagane.", file=sys.stderr)
        sys.exit(1)

    columns = ", ".join(to_insert.keys())
    placeholders = ", ".join(["?"] * len(to_insert))
    sql = f"INSERT INTO items ({columns}) VALUES ({placeholders})"

    try:
        conn.execute(sql, list(to_insert.values()))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"ERROR: Nie udało się wstawić rekordu: {e}", file=sys.stderr)
        sys.exit(1)

    print("OK: added item.")
    print(f"  slug: {slug}")
    print(f"  name: {name}")


def list_items(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    limit_clause = ""
    params = []
    if args.limit is not None:
        limit_clause = "LIMIT ?"
        params.append(args.limit)

    sql = f"""
        SELECT id, slug, name, rarity, category, value, weight, stack_size
        FROM items
        ORDER BY id ASC
        {limit_clause}
    """

    cur = conn.execute(sql, params)
    rows = cur.fetchall()

    if not rows:
        print("Brak itemów w tabeli 'items'.")
        return

    for row in rows:
        print(
            f"[{row['id']}] {row['slug']} | {row['name']} "
            f"(rarity={row['rarity']}, cat={row['category']}, "
            f"value={row['value']}, weight={row['weight']}, stack={row['stack_size']})"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI do zarządzania tabelą 'items' w bazie SQLite."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- subkomenda: add ---
    add_parser = subparsers.add_parser("add", help="Dodaj nowy item do tabeli items.")

    add_parser.add_argument(
        "--name",
        required=True,
        help='np. "Looting MK.2"'
    )
    add_parser.add_argument(
        "--description",
        help="Opis przedmiotu."
    )
    add_parser.add_argument(
        "--rarity",
        required=True,
        help="Rzadkość (np. common/rare/epic)."
    )
    add_parser.add_argument(
        "--value",
        required=True,
        type=int,
        help="Value in scraps",
    )
    add_parser.add_argument(
        "--weight",
        required=True,
        type=float,
        help="Wight (float).",
    )
    add_parser.add_argument(
        "--category",
        required=True,
        help="In-game category",
    )
    add_parser.add_argument(
        "--stack-size",
        type=int,
        dest="stack_size",
        help="Max stack (default 1)",
        default=1
    )
    add_parser.set_defaults(func=add_item)

    # --- subkomenda: list ---
    list_parser = subparsers.add_parser(
        "list", help="Wypisz istniejące itemy (skrótowo)."
    )
    list_parser.add_argument(
        "--limit",
        type=int,
        help="Ogranicz liczbę wypisywanych wierszy.",
    )
    list_parser.set_defaults(func=list_items)

    return parser


def main() -> None:

    parser = build_parser()
    args = parser.parse_args()

    conn = connect_db(SQLITE_DATABASE)
    ensure_items_table(conn)

    # Wywołujemy odpowiednią funkcję dla subkomendy
    args.func(conn, args)


if __name__ == "__main__":
    main()
