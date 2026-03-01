# pramana-python-sdk

Python SDK for the [Pramana](https://pramana.dev) knowledge graph. Provides exact-arithmetic value types, item model mapping, and data source connectors for working with Pramana data in Python.

## Status

**Early development** - Gaussian integer and rational arithmetic is implemented. ORM mapping and data sources are planned.

## Installation

```bash
pip install pramana-lib
```

For development:

```bash
pip install -e .
```

## Gaussian Integers & Rationals

The Pramana standard names are **`Gauss`** (Gaussian rational, Q[i]) and **`Gint`** (Gaussian integer, Z[i]). The mathematical names `Qi` and `Zi` are also available as aliases.

The SDK includes `Gauss`/`Qi` (Gaussian rationals) and `Gint`/`Zi` (Gaussian integers) classes providing exact arithmetic for complex numbers with integer or rational components.

These classes are forked from [gaussian_integers](https://github.com/alreich/gaussian_integers) by **Alfred J. Reich, Ph.D.**, used under the MIT license. Dr. Reich's implementation provides exact arithmetic, number-theoretic operations (GCD, Extended Euclidean Algorithm, Gaussian primality testing), and the Modified Division Theorem based on Keith Conrad's ["The Gaussian Integers"](https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf). See [NOTICE.md](NOTICE.md) for full attribution.

### Quick Example

```python
from pramana import Gauss, Gint

# Gaussian integer arithmetic
alpha = Gint(11, 3)   # 11 + 3i
beta = Gint(1, 8)     # 1 + 8i

# Extended Euclidean Algorithm (Bezout coefficients)
gcd, x, y = Gint.xgcd(alpha, beta)
print(f"{alpha * x + beta * y} = {alpha} * {x} + {beta} * {y}")
# (1-2j) = (11+3j) * (2-1j) + (1+8j) * 3j

# Gaussian rational arithmetic (exact fractions)
r = Gauss(2, 3.4)          # 2 + 17/5 i
s = Gauss("4/6", "-1/7")   # 2/3 - 1/7 i
print(r * s)                # exact rational result

# Division returns Gauss when not exact, Gint when it is
print(Gint(4, 5) / Gint(1, -2))  # Qi('-6/5', '13/5')
print(Gint(4, 8) / 2)            # Zi(2, 4)

# Primality testing
print(Gint.is_gaussian_prime(3))  # True (3 ≡ 3 mod 4)
print(Gint.is_gaussian_prime(5))  # False (5 = (2+i)(2-i))
```

## Key Features (Planned)

- **Pramana GaussianRational** - The `(A,B,C,D)` canonical form with UUID v5 identity, built on top of Gauss/Gint
- **Deterministic Pramana IDs** - UUID v5 generation matching the canonical Pramana web app
- **ORM-style entity mapping** - `@pramana_entity` decorator with proposition-backed fields
- **Multiple data sources** - `.pra` files, SPARQL, REST API, SQLite

## Running Tests

```bash
pip install -e .
pytest
```

## Documentation

- [General SDK Specification](08_SDK_LIBRARY_SPECIFICATION.md) - Cross-language design spec
- [Python Implementation Guide](IMPLEMENTATION.md) - Python-specific implementation details
- [NOTICE.md](NOTICE.md) - Third-party attribution

## Pramana SDK Family

| Language | Repository | Package |
|----------|-----------|---------|
| C# / .NET | [pramana-dotnet-sdk](https://github.com/Emma-Leonhart/pramana-dotnet-sdk) | `Pramana.SDK` (NuGet) |
| Python | **pramana-python-sdk** (this repo) | `pramana-lib` (PyPI) |
| npm (TypeScript or JavaScript) | [pramana-npm-sdk](https://github.com/Emma-Leonhart/pramana-ts-sdk) | `@pramana/sdk` (npm) |
| Java | [pramana-java-sdk](https://github.com/Emma-Leonhart/pramana-java-sdk) | `org.pramana:pramana-sdk` (Maven) |
| Rust | [pramana-rust-sdk](https://github.com/Emma-Leonhart/pramana-rust-sdk) | `pramana-sdk` (crates.io) |
| Go | [pramana-go-sdk](https://github.com/Emma-Leonhart/pramana-go-sdk) | `github.com/Emma-Leonhart/pramana-go-sdk` |

All SDKs implement the same core specification and must produce identical results for UUID v5 generation, canonical string normalization, and arithmetic operations.
