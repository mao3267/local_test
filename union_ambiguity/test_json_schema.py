from typing import List, Dict, Union, cast, Optional, Tuple
from mashumaro.mixins.json import DataClassJSONMixin
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from mashumaro.jsonschema import build_json_schema
from flytekit.core.type_engine import DataclassTransformer
from pydantic import BaseModel

@dataclass
class A:
    a: int
@dataclass
class Inner:
    a: A
    b: A
    c: A
@dataclass
class A:
    a: Tuple[int, int, Optional[int]]
    inner: Inner


schema = build_json_schema(cast(DataClassJSONMixin, DataclassTransformer()._get_origin_type_in_annotation(A))).to_dict()
print(schema)

