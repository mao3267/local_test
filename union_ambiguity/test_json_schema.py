from typing import List, Dict, Union, cast, Optional
from mashumaro.mixins.json import DataClassJSONMixin
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from mashumaro.jsonschema import build_json_schema
from flytekit.core.type_engine import DataclassTransformer
from pydantic import BaseModel


class A(BaseModel):
    a: Optional[int]

@dataclass_json
@dataclass
class B:
    b: Optional[int]

schema = build_json_schema(cast(DataClassJSONMixin, DataclassTransformer()._get_origin_type_in_annotation(A))).to_dict()
print(schema)

