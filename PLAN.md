# nestpath release plan

## PM stage

### Chosen idea
A tiny Python package for nested dict/list access via dot paths.

### Why this idea
- Common pain point in JSON/config manipulation
- Easy to understand in one glance
- Narrow enough for a polished one-run MVP
- Useful without requiring framework coupling

### MVP scope
- Parse dot paths with list indices
- Read values
- Write values with automatic container creation
- Check path existence
- Delete values
- English README
- Minimal CI

### Non-goals
- Wildcards
- Negative indices
- Slice syntax
- Attribute access
- Pydantic/dataclass integration
- Schema validation

## Spec / design stage

### DX goals
- Single import, tiny API surface
- Works on plain Python dict/list objects
- Predictable exceptions
- No dependencies

### Public API shape
- `parse_path(path)`
- `get_path(data, path, default=_MISSING)`
- `set_path(data, path, value)`
- `has_path(data, path)`
- `delete_path(data, path)`

### README structure
1. Problem / why
2. Features
3. Installation
4. Quick start
5. API reference
6. Path syntax
7. Limitations
8. Development
9. License

### Package architecture
- `src/nestpath/__init__.py` exports public API
- `src/nestpath/core.py` contains implementation
- `tests/test_core.py` covers parsing and CRUD behavior
- `.github/workflows/ci.yml` runs unittest matrix

## Acceptance checklist
- Repository has standard Python package layout
- Tests pass locally
- README explains scope and limitations
- CI file prepared
- Caveats explicitly documented
