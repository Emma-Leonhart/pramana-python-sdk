# pramana-python-sdk

Python SDK for the [Pramana](https://pramana-data.ca) knowledge graph. Provides exact-arithmetic value types, item model mapping, and data source connectors for working with Pramana data in Python.

## Status

**Early development** - Gaussian integer and rational arithmetic is implemented. ORM mapping and data sources are planned.

## Installation

```bash
pip install -e .
```

## Gaussian Integers & Rationals

The standard short name for a Gaussian rational in Pramana is **`Gauss`**, and for a Gaussian integer it is **`Gint`**. The Python SDK currently uses `Qi` (Q[i]) and `Zi` (Z[i]) as class names from the upstream library, which correspond to `Gauss` and `Gint` respectively.

The SDK includes `Zi` (Gaussian integers, Z[i] / **Gint**) and `Qi` (Gaussian rationals, Q[i] / **Gauss**) classes providing exact arithmetic for complex numbers with integer or rational components.

These classes are forked from [gaussian_integers](https://github.com/alreich/gaussian_integers) by **Alfred J. Reich, Ph.D.**, used under the MIT license. Dr. Reich's implementation provides exact arithmetic, number-theoretic operations (GCD, Extended Euclidean Algorithm, Gaussian primality testing), and the Modified Division Theorem based on Keith Conrad's ["The Gaussian Integers"](https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf). See [NOTICE.md](NOTICE.md) for full attribution.

### Quick Example

```python
from pramana.gaussians import Zi, Qi

# Gaussian integer arithmetic
alpha = Zi(11, 3)   # 11 + 3i
beta = Zi(1, 8)     # 1 + 8i

# Extended Euclidean Algorithm (Bezout coefficients)
gcd, x, y = Zi.xgcd(alpha, beta)
print(f"{alpha * x + beta * y} = {alpha} * {x} + {beta} * {y}")
# (1-2j) = (11+3j) * (2-1j) + (1+8j) * 3j

# Gaussian rational arithmetic (exact fractions)
r = Qi(2, 3.4)          # 2 + 17/5 i
s = Qi("4/6", "-1/7")   # 2/3 - 1/7 i
print(r * s)             # exact rational result

# Division returns Qi when not exact, Zi when it is
print(Zi(4, 5) / Zi(1, -2))  # Qi('-6/5', '13/5')
print(Zi(4, 8) / 2)          # Zi(2, 4)

# Primality testing
print(Zi.is_gaussian_prime(3))  # True (3 ≡ 3 mod 4)
print(Zi.is_gaussian_prime(5))  # False (5 = (2+i)(2-i))
```

## Key Features (Planned)

- **Pramana GaussianRational** - The `(A,B,C,D)` canonical form with UUID v5 identity, built on top of Zi/Qi
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
| Python | **pramana-python-sdk** (this repo) | `pramana-sdk` (PyPI) |
| TypeScript | [pramana-ts-sdk](https://github.com/Emma-Leonhart/pramana-ts-sdk) | `@pramana/sdk` (npm) |
| JavaScript | [pramana-js-sdk](https://github.com/Emma-Leonhart/pramana-js-sdk) | `@pramana/sdk` (npm) |
| Java | [pramana-java-sdk](https://github.com/Emma-Leonhart/pramana-java-sdk) | `org.pramana:pramana-sdk` (Maven) |
| Rust | [pramana-rust-sdk](https://github.com/Emma-Leonhart/pramana-rust-sdk) | `pramana-sdk` (crates.io) |
| Go | [pramana-go-sdk](https://github.com/Emma-Leonhart/pramana-go-sdk) | `github.com/Emma-Leonhart/pramana-go-sdk` |

All SDKs implement the same core specification and must produce identical results for UUID v5 generation, canonical string normalization, and arithmetic operations.
