# Pramana Python SDK - Implementation Guide

**Package name:** `pramana-sdk` (PyPI) / `import pramana`
**Minimum Python:** 3.11+
**Reference implementation:** [PramanaLib (C#)](https://github.com/Emma-Leonhart/PramanaLib)

---

## 1. Project Structure

```
pramana-python-sdk/
├── pyproject.toml              # Build configuration (PEP 621)
├── src/
│   └── pramana/
│       ├── __init__.py         # Public API re-exports
│       ├── py.typed            # PEP 561 type marker
│       ├── gaussian_rational.py    # GaussianRational implementation
│       ├── pramana_id.py       # UUID v5 generation utilities
│       ├── item.py             # PramanaItem base class
│       ├── entity.py           # PramanaEntity
│       ├── property.py         # PramanaProperty
│       ├── proposition.py      # PramanaProposition
│       ├── sense.py            # PramanaSense
│       ├── orm/
│       │   ├── __init__.py
│       │   ├── decorators.py   # @pramana_entity, @pramana_property decorators
│       │   ├── config.py       # PramanaConfig
│       │   ├── query.py        # Query builder interface
│       │   └── mapping.py      # Field-to-proposition mapping logic
│       ├── datasources/
│       │   ├── __init__.py
│       │   ├── pra_file.py     # .pra JSON file reader
│       │   ├── sparql.py       # GraphDB SPARQL connector
│       │   ├── rest_api.py     # Pramana REST API connector
│       │   └── sqlite.py       # SQLite export reader
│       └── structs/
│           ├── __init__.py
│           ├── date.py         # date: pseudo-class
│           ├── time.py         # time: pseudo-class
│           ├── interval.py     # interval: pseudo-class
│           ├── coordinate.py   # coord: pseudo-class
│           └── chemical.py     # chem: / element: pseudo-classes
├── tests/
│   ├── test_gaussian_rational.py
│   ├── test_pramana_id.py
│   ├── test_item_model.py
│   ├── test_orm.py
│   ├── test_serialization.py
│   └── test_vectors.json       # Cross-language test vectors
└── docs/
    └── api.md
```

## 2. Build & Packaging

### pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "pramana-sdk"
version = "0.1.0"
description = "Python SDK for the Pramana knowledge graph"
requires-python = ">=3.11"
license = "MIT"
authors = [
    { name = "Pramana Contributors" }
]
dependencies = []

[project.optional-dependencies]
sparql = ["SPARQLWrapper>=2.0"]
api = ["httpx>=0.25"]
all = ["pramana-sdk[sparql,api]"]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "mypy",
    "ruff",
]

[tool.hatch.build.targets.wheel]
packages = ["src/pramana"]

[tool.mypy]
strict = true

[tool.ruff]
target-version = "py311"
```

### Key decisions:
- **Zero runtime dependencies** for core (GaussianRational, item model, .pra files)
- Optional extras for SPARQL, REST API connectors
- `src/` layout (PEP 517 best practice)
- Hatchling build backend (modern, fast)

## 3. GaussianRational (Gauss) Implementation

> **Naming convention:** The standard short name for a Gaussian rational is **`Gauss`** (corresponds to `Qi` in the current Python implementation). When referring specifically to a Gaussian integer (both denominators are 1), the standard short name is **`Gint`** (corresponds to `Zi`).

### 3.1 Class Design

Python's `int` has native arbitrary precision, so no BigInt library is needed.

```python
from __future__ import annotations
import math
import uuid
import hashlib
from dataclasses import dataclass
from typing import Self
from enum import Enum

class NumberType(Enum):
    NATURAL_NUMBER = "Natural Number"
    WHOLE_NUMBER = "Whole Number"
    INTEGER = "Integer"
    RATIONAL_NUMBER = "Rational Number"
    GAUSSIAN_RATIONAL = "Gaussian Rational"


@dataclass(frozen=True, slots=True)
class GaussianRational:
    """Exact complex rational number: a/b + (c/d)i"""
    a: int  # real numerator
    b: int  # real denominator (positive, nonzero)
    c: int  # imaginary numerator
    d: int  # imaginary denominator (positive, nonzero)

    def __post_init__(self) -> None:
        if self.b <= 0 or self.d <= 0:
            raise ValueError("Denominators must be positive integers")
        # Normalize to canonical form
        g_real = math.gcd(abs(self.a), self.b)
        g_imag = math.gcd(abs(self.c), self.d)
        object.__setattr__(self, 'a', self.a // g_real)
        object.__setattr__(self, 'b', self.b // g_real)
        object.__setattr__(self, 'c', self.c // g_imag)
        object.__setattr__(self, 'd', self.d // g_imag)
```

### 3.2 Constructors

```python
    @classmethod
    def from_int(cls, value: int) -> Self:
        """Create from a single integer (imaginary = 0)."""
        return cls(value, 1, 0, 1)

    @classmethod
    def from_complex(cls, real: int, imag: int) -> Self:
        """Create from integer real and imaginary parts."""
        return cls(real, 1, imag, 1)

    @classmethod
    def parse(cls, s: str) -> Self:
        """Parse from canonical 'a,b,c,d' or 'num:a,b,c,d' string."""
        s = s.removeprefix("num:")
        parts = s.split(",")
        if len(parts) != 4:
            raise ValueError(f"Expected 4 comma-separated integers, got: {s}")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
```

### 3.3 Operator Overloading

Python supports full operator overloading via dunder methods:

```python
    def __add__(self, other: GaussianRational) -> GaussianRational:
        # a1/b1 + a2/b2 = (a1*b2 + a2*b1) / (b1*b2)
        real_num = self.a * other.b + other.a * self.b
        real_den = self.b * other.b
        imag_num = self.c * other.d + other.c * self.d
        imag_den = self.d * other.d
        return GaussianRational(real_num, real_den, imag_num, imag_den)

    def __sub__(self, other: GaussianRational) -> GaussianRational: ...
    def __neg__(self) -> GaussianRational: ...
    def __mul__(self, other: GaussianRational) -> GaussianRational:
        # (a+bi)(c+di) = (ac-bd) + (ad+bc)i
        ...
    def __truediv__(self, other: GaussianRational) -> GaussianRational:
        # Multiply by conjugate, divide
        ...
    def __mod__(self, other: GaussianRational) -> GaussianRational:
        # Real-only; raise for complex
        ...
    def __pow__(self, exp: int) -> GaussianRational:
        # Integer exponents only
        ...
    def __eq__(self, other: object) -> bool:
        # Component-wise after normalization
        ...
    def __lt__(self, other: GaussianRational) -> bool:
        # Real values only; raise for complex
        ...
    def __le__(self, other: GaussianRational) -> bool: ...
    def __gt__(self, other: GaussianRational) -> bool: ...
    def __ge__(self, other: GaussianRational) -> bool: ...
    def __hash__(self) -> int:
        return hash((self.a, self.b, self.c, self.d))
```

### 3.4 Properties

```python
    @property
    def is_real(self) -> bool:
        return self.c == 0

    @property
    def is_integer(self) -> bool:
        return self.is_real and self.b == 1

    @property
    def is_gaussian_integer(self) -> bool:
        return self.b == 1 and self.d == 1

    @property
    def is_zero(self) -> bool:
        return self.a == 0 and self.c == 0

    @property
    def is_positive(self) -> bool:
        return self.is_real and self.a > 0

    @property
    def is_negative(self) -> bool:
        return self.is_real and self.a < 0

    @property
    def conjugate(self) -> GaussianRational:
        return GaussianRational(self.a, self.b, -self.c, self.d)

    @property
    def magnitude_squared(self) -> GaussianRational:
        # (a/b)^2 + (c/d)^2 — exact, returns real GaussianRational
        ...

    @property
    def real_part(self) -> GaussianRational:
        return GaussianRational(self.a, self.b, 0, 1)

    @property
    def imaginary_part(self) -> GaussianRational:
        return GaussianRational(self.c, self.d, 0, 1)

    @property
    def reciprocal(self) -> GaussianRational:
        # 1/z via conjugate method
        ...

    def classify(self) -> NumberType:
        if not self.is_real:
            return NumberType.GAUSSIAN_RATIONAL
        if not self.is_integer:
            return NumberType.RATIONAL_NUMBER
        if self.a > 0:
            return NumberType.NATURAL_NUMBER
        if self.a >= 0:
            return NumberType.WHOLE_NUMBER
        return NumberType.INTEGER
```

### 3.5 Pramana ID (UUID v5)

```python
    NUM_NAMESPACE = uuid.UUID("a6613321-e9f6-4348-8f8b-29d2a3c86349")

    @property
    def canonical(self) -> str:
        """Canonical num: string representation."""
        return f"num:{self.a},{self.b},{self.c},{self.d}"

    @property
    def pramana_id(self) -> uuid.UUID:
        """Deterministic UUID v5 from canonical representation."""
        return uuid.uuid5(self.NUM_NAMESPACE, self.canonical)

    @property
    def pramana_uri(self) -> str:
        return f"pra:{self.pramana_id}"
```

Python's `uuid.uuid5()` handles the UUID v5 algorithm natively. This is one of the simplest implementations across all languages.

### 3.6 Formatting

```python
    def to_mixed(self) -> str:
        """Human-readable mixed fraction: '3 & 1/2 + 3/4 i'"""
        ...

    def to_improper(self) -> str:
        """Improper fraction: '7/2 + 3/4 i'"""
        ...

    def to_raw(self) -> str:
        """Component tuple: '<7,2,3,4>'"""
        return f"<{self.a},{self.b},{self.c},{self.d}>"

    def __str__(self) -> str:
        return self.canonical

    def __repr__(self) -> str:
        return f"GaussianRational({self.a}, {self.b}, {self.c}, {self.d})"
```

### 3.7 Intentionally Unsupported

These must raise `NotImplementedError`:

```python
    def __abs__(self) -> None:
        raise NotImplementedError(
            "Complex magnitude produces irrationals. Use magnitude_squared for exact result."
        )

    # sqrt, phase/arg, to_polar — same treatment
```

## 4. Item Model

### 4.1 Base Type

```python
from enum import Enum
from typing import Any

class ItemType(Enum):
    ENTITY = "Entity"
    PROPERTY = "Property"
    PROPOSITION = "Proposition"
    SENSE = "Sense"
    EVIDENCE = "Evidence"
    STANCE_LINK = "StanceLink"


@dataclass
class PramanaItem:
    uuid: uuid.UUID
    type: ItemType
    properties: dict[str, Any]
    edges: dict[str, uuid.UUID]
```

### 4.2 Typed Wrappers

```python
@dataclass
class PramanaEntity(PramanaItem):
    label: str = ""
    _instance_of: uuid.UUID | None = None  # lazy
    _propositions: list[PramanaProposition] | None = None  # lazy

    @property
    def instance_of(self) -> PramanaEntity | None:
        # Lazy resolution via graph context
        ...
```

### 4.3 JSON Serialization

```python
import json
from pathlib import Path

class PramanaGraph:
    @classmethod
    def from_file(cls, path: str | Path) -> PramanaGraph:
        """Load from .pra JSON file."""
        with open(path) as f:
            data = json.load(f)
        ...

    def to_file(self, path: str | Path) -> None:
        """Serialize to .pra JSON file."""
        ...
```

## 5. ORM-Style Mapping

### 5.1 Decorators

```python
from pramana.orm import pramana_entity, pramana_property, computed_property

@pramana_entity(instance_of="uuid-of-shinto-shrine-class")
class ShintoShrine:
    name: str
    coordinates: Coordinate | None = None
    wikidata_id: str | None = None
    part_of: ShintoShrine | None = None

    @computed_property("age")
    def age(self) -> int:
        return (date.today() - self.date_of_birth).days // 365
```

Internally, `@pramana_entity` uses `__init_subclass__` or a metaclass to:
1. Inspect type annotations to build the field-to-property mapping
2. Register the class in a global type registry
3. Generate `__init__`, property accessors, and proposition-aware setters

### 5.2 Decorator Implementation Approach

Use **descriptor protocol** for property fields:

```python
class PramanaField:
    """Descriptor that maps a class field to a Pramana proposition."""
    def __init__(self, property_name: str, *, required: bool = False, multiple: bool = False):
        self.property_name = property_name
        self.required = required
        self.multiple = multiple

    def __set_name__(self, owner: type, name: str) -> None:
        self.field_name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        # Look up proposition value from obj's proposition store
        ...

    def __set__(self, obj: Any, value: Any) -> None:
        # Create/update proposition
        ...
```

### 5.3 Query Interface

```python
shrines = pramana.query(ShintoShrine).filter(coordinates__not_null=True).all()
water = pramana.get_by_id("00000007-...", as_type=ChemicalCompound)
```

Query builder uses Django-style double-underscore filters internally, translating to SPARQL or REST API calls depending on the configured data source.

### 5.4 Configuration

```python
from pramana.orm import PramanaConfig

config = PramanaConfig(
    flatten_depth=3,
    lazy_resolve=True,
    include_provenance=False,
)
```

## 6. Data Sources

| Source | Module | Extra dependency |
|--------|--------|-----------------|
| `.pra` JSON file | `pramana.datasources.pra_file` | None |
| GraphDB SPARQL | `pramana.datasources.sparql` | `SPARQLWrapper` |
| Pramana REST API | `pramana.datasources.rest_api` | `httpx` |
| SQLite export | `pramana.datasources.sqlite` | None (stdlib `sqlite3`) |

```python
graph = PramanaGraph.from_file("foundation.pra")
graph = PramanaGraph.from_sparql("http://localhost:7200/repositories/pramana")
graph = PramanaGraph.from_api("https://pramana.dev")
```

## 7. Struct Pseudo-Classes

| Pseudo-class | Python type | Mapping strategy |
|-------------|-------------|-----------------|
| `num:` | `GaussianRational` | Custom class (see above) |
| `date:` | `datetime.date` | Wrapper with `pramana_id` property |
| `time:` | `datetime.time` | Wrapper with `pramana_id` property |
| `interval:` | Tuple of `datetime.date` | Custom `PramanaInterval` dataclass |
| `coord:` | `PramanaCoordinate` | Simple `(lat, lon)` dataclass |
| `chem:` | `str` (InChI) | Wrapper with `pramana_id` property |
| `element:` | `int` (atomic number) | Wrapper with `pramana_id` property |

Each pseudo-class wrapper generates its UUID v5 using the namespace UUID from the spec and Python's `uuid.uuid5()`.

## 8. Testing Strategy

- **pytest** as test runner
- **Cross-language test vectors** loaded from `tests/test_vectors.json`
- Test categories:
  1. `test_gaussian_rational.py` — arithmetic, normalization, properties, classification
  2. `test_pramana_id.py` — UUID v5 generation matches reference implementation
  3. `test_item_model.py` — serialization roundtrip, type mapping
  4. `test_orm.py` — decorator registration, field descriptors, query building
  5. `test_serialization.py` — .pra file load/save roundtrip

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=pramana --cov-report=term-missing

# Type checking
mypy src/pramana/
```

## 9. Implementation Priority

### Phase 1 - GaussianRational (core)
1. Implement `GaussianRational` frozen dataclass with all arithmetic operators
2. Implement `uuid.uuid5()` based Pramana ID generation
3. Implement `parse()`, formatting methods, and `classify()`
4. Write comprehensive test suite against test vectors

### Phase 2 - Base Item Model
1. Implement `PramanaItem`, `PramanaEntity`, `PramanaProperty`, `PramanaProposition`, `PramanaSense`
2. Implement JSON serialization compatible with `.pra` format
3. Implement `.pra` file reader/writer

### Phase 3 - ORM Mapping
1. Implement `@pramana_entity` decorator and `PramanaField` descriptor
2. Implement `PramanaConfig` with flattening depth and lazy resolution
3. Implement query builder interface

### Phase 4 - Data Sources & Provenance
1. SPARQL connector (SPARQLWrapper)
2. REST API connector (httpx)
3. Evidence/provenance metadata on fields

### Phase 5 - Pseudo-Classes
1. `date:`, `time:`, `interval:` wrappers
2. `coord:` struct
3. `chem:` / `element:` wrappers

## 10. Python-Specific Advantages

- **Native arbitrary-precision integers** — no external BigInt library needed
- **Built-in `uuid.uuid5()`** — simplest UUID v5 implementation across all SDKs
- **`@dataclass(frozen=True, slots=True)`** — immutable value types with minimal boilerplate
- **Full operator overloading** — `+`, `-`, `*`, `/`, `%`, `**`, `==`, `<`, etc.
- **Descriptor protocol** — clean ORM field mapping without metaclass complexity
- **Type hints + `py.typed`** — first-class IDE support and static analysis
- **`__init_subclass__`** — modern hook for decorator-based class registration
