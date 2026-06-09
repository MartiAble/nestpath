# nestpath

Tiny Python helpers for reading, writing, checking, and deleting values inside nested `dict` / `list` structures with dot paths like `users[0].email`.

`nestpath` is intentionally small: no query language, no schema system, no magic models — just a predictable path API for plain Python data.

## Why

Working with JSON-like Python objects often turns into repetitive guard code:

- check if a nested key exists
- create missing containers
- handle list indices
- safely return a default when a path is missing

`nestpath` wraps that into a compact MVP API.

## Features

- Read nested values with a dot path
- Write nested values and auto-create missing containers
- Check whether a path exists
- Delete nested keys or list items
- Support escaped dots in dictionary keys (`theme\.dark`)
- Zero runtime dependencies

## Installation

```bash
pip install nestpath
```

## Quick start

```python
from nestpath import get_path, set_path, has_path, delete_path

data = {}
set_path(data, "users[0].profile.email", "alice@example.com")

assert data == {
    "users": [
        {"profile": {"email": "alice@example.com"}}
    ]
}

assert get_path(data, "users[0].profile.email") == "alice@example.com"
assert has_path(data, "users[0].profile.email") is True
assert get_path(data, "users[0].profile.name", default="unknown") == "unknown"

remove_ok = delete_path(data, "users[0].profile.email")
assert remove_ok is True
```

## API

### `parse_path(path: str) -> list[str | int]`

Parses a path string into tokens.

```python
parse_path("users[0].email")
# ["users", 0, "email"]
```

### `get_path(data, path, default=_MISSING)`

Returns the value at `path`.

- If `default` is provided and the path is missing, returns `default`
- Otherwise raises `KeyError`

### `set_path(data, path, value)`

Writes `value` at `path` and creates missing intermediate containers.

- Creates `dict` when the next token is a key
- Creates `list` when the next token is an index
- Raises `TypeError` on container type mismatches

### `has_path(data, path) -> bool`

Returns `True` if the path exists, otherwise `False`.

### `delete_path(data, path) -> bool`

Deletes the value at `path`.

- Returns `True` when something was removed
- Returns `False` when the path does not exist or the container type does not match

## Path syntax

Supported syntax:

- `user.profile.name`
- `users[0].email`
- `settings.theme\.dark.enabled` for literal dots in keys

Current limitations:

- Only non-negative list indices are supported
- Bracket notation is only for numeric list indices
- Escape handling is intentionally minimal and only targets literal special characters

## DX and design notes

This package is optimized for:

- small scripts
- API clients
- config/JSON transformations
- test fixtures
- internal tools that need a tiny dependency

It is **not** trying to replace full-featured object query libraries.

## Development

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Release checklist

- [x] Define narrow MVP
- [x] Implement core path parsing and CRUD helpers
- [x] Add unit tests
- [x] Write README in English
- [x] Add GitHub Actions CI
- [x] Create public GitHub repository

## License

MIT
