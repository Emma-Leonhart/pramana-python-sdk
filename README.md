# pramana-python-sdk

Python SDK for the [Pramana](https://pramana-data.ca) knowledge graph. Provides exact-arithmetic value types, item model mapping, and data source connectors for working with Pramana data in Python.

## Status

**Pre-implementation** - Project structure and implementation plan documented. See [IMPLEMENTATION.md](IMPLEMENTATION.md) for the full design.

## Key Features (Planned)

- **GaussianRational** - Exact complex rational arithmetic (`a/b + (c/d)i`) with native Python arbitrary-precision integers
- **Deterministic Pramana IDs** - UUID v5 generation matching the canonical Pramana web app
- **Full operator overloading** - `+`, `-`, `*`, `/`, `%`, `**`, `==`, `<`, etc.
- **ORM-style entity mapping** - `@pramana_entity` decorator with proposition-backed fields
- **Multiple data sources** - `.pra` files, SPARQL, REST API, SQLite

## Installation (Future)

```bash
pip install pramana-sdk
```

## Quick Example (Planned API)

```python
from pramana import GaussianRational

half = GaussianRational(1, 2, 0, 1)    # 1/2
third = GaussianRational(1, 3, 0, 1)   # 1/3
result = half + third                    # 5/6

print(result.pramana_id)  # deterministic UUID v5
```

## Documentation

- [General SDK Specification](08_SDK_LIBRARY_SPECIFICATION.md) - Cross-language design spec
- [Python Implementation Guide](IMPLEMENTATION.md) - Python-specific implementation details

## Pramana SDK Family

| Language | Repository | Package |
|----------|-----------|---------|
| C# / .NET | [pramana-dotnet-sdk](https://github.com/Emma-Leonhart/pramana-dotnet-sdk) | `Pramana.SDK` (NuGet) |
| Python | **pramana-python-sdk** (this repo) | `pramana-sdk` (PyPI) |
| TypeScript | [pramana-ts-sdk](https://github.com/Emma-Leonhart/pramana-ts-sdk) | `@pramana/sdk` (npm) |
| JavaScript | [pramana-js-sdk](https://github.com/Emma-Leonhart/pramana-js-sdk) | `@pramana/sdk` (npm) |
| Java | [pramana-java-sdk](https://github.com/Emma-Leonhart/pramana-java-sdk) | `org.pramana:pramana-sdk` (Maven) |
| Rust | [pramana-rust-sdk](https://github.com/Emma-Leonhart/pramana-rust-sdk) | `pramana-sdk` (crates.io) |
| Go | [pramana-go-sdk](https://github.com/Emma-Leonhart/pramana-go-sdk) | `github.com/Emma-Leonhart/pramana-go-sdk` |

All SDKs implement the same core specification and must produce identical results for UUID v5 generation, canonical string normalization, and arithmetic operations.
