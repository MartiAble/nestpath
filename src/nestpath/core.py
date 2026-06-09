from __future__ import annotations

from typing import Any, Iterable, List, Sequence, Union

Token = Union[str, int]
_MISSING = object()


class PathSyntaxError(ValueError):
    """Raised when a path expression cannot be parsed."""


def parse_path(path: str) -> List[Token]:
    """Parse a dot path like ``users[0].email`` into tokens.

    Supported syntax:
    - Dots separate dictionary keys.
    - Brackets access list indices, e.g. ``items[2]``.
    - A backslash escapes a literal dot or bracket inside a key.
    """
    if not isinstance(path, str) or not path:
        raise PathSyntaxError("path must be a non-empty string")

    tokens: List[Token] = []
    key: List[str] = []
    i = 0
    length = len(path)

    def flush_key() -> None:
        if key:
            tokens.append("".join(key))
            key.clear()

    last_was_index = False

    while i < length:
        char = path[i]

        if char == "\\":
            i += 1
            if i >= length:
                raise PathSyntaxError("dangling escape at end of path")
            key.append(path[i])
            last_was_index = False
        elif char == ".":
            if key:
                flush_key()
            elif not last_was_index:
                raise PathSyntaxError("empty key segment in path")
            last_was_index = False
        elif char == "[":
            flush_key()
            end = path.find("]", i + 1)
            if end == -1:
                raise PathSyntaxError("unclosed bracket in path")
            index_text = path[i + 1 : end]
            if not index_text or not index_text.isdigit():
                raise PathSyntaxError("list indices must be non-negative integers")
            tokens.append(int(index_text))
            last_was_index = True
            i = end
        elif char == "]":
            raise PathSyntaxError("unexpected closing bracket in path")
        else:
            key.append(char)
            last_was_index = False
        i += 1

    flush_key()

    if not tokens:
        raise PathSyntaxError("path produced no tokens")

    return tokens


def _container_for(next_token: Token) -> Any:
    return [] if isinstance(next_token, int) else {}


def _ensure_list_size(items: list[Any], index: int, fill: Any = _MISSING) -> None:
    while len(items) <= index:
        items.append(None if fill is _MISSING else fill)


def get_path(data: Any, path: str, default: Any = _MISSING) -> Any:
    current = data
    for token in parse_path(path):
        try:
            current = current[token]
        except (KeyError, IndexError, TypeError):
            if default is _MISSING:
                raise KeyError(path) from None
            return default
    return current


def has_path(data: Any, path: str) -> bool:
    try:
        get_path(data, path)
        return True
    except KeyError:
        return False


def set_path(data: Any, path: str, value: Any) -> Any:
    tokens = parse_path(path)
    current = data

    for position, token in enumerate(tokens[:-1]):
        next_token = tokens[position + 1]

        if isinstance(token, int):
            if not isinstance(current, list):
                raise TypeError(f"expected list at token {token}, got {type(current).__name__}")
            _ensure_list_size(current, token)
            if current[token] is None:
                current[token] = _container_for(next_token)
            current = current[token]
        else:
            if not isinstance(current, dict):
                raise TypeError(f"expected dict at key {token!r}, got {type(current).__name__}")
            if token not in current or current[token] is None:
                current[token] = _container_for(next_token)
            current = current[token]

    last = tokens[-1]
    if isinstance(last, int):
        if not isinstance(current, list):
            raise TypeError(f"expected list at final token {last}, got {type(current).__name__}")
        _ensure_list_size(current, last)
        current[last] = value
    else:
        if not isinstance(current, dict):
            raise TypeError(f"expected dict at final key {last!r}, got {type(current).__name__}")
        current[last] = value
    return data


def delete_path(data: Any, path: str) -> bool:
    tokens = parse_path(path)
    current = data

    for token in tokens[:-1]:
        try:
            current = current[token]
        except (KeyError, IndexError, TypeError):
            return False

    last = tokens[-1]
    try:
        if isinstance(last, int):
            if not isinstance(current, list):
                return False
            del current[last]
        else:
            if not isinstance(current, dict):
                return False
            del current[last]
        return True
    except (KeyError, IndexError, TypeError):
        return False
