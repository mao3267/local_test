from mashumaro.codecs.msgpack import MessagePackDecoder, MessagePackEncoder
from dataclasses import dataclass
from typing import Any, Union
import msgpack

def _default_msgpack_decoder(data: bytes) -> Any:
    return msgpack.unpackb(data, raw=False, strict_map_key=False)

@dataclass
class A:
    a: int

@dataclass
class InnerDC:
    a: Union[str, A]

@dataclass
class DC:
    inner_dc: InnerDC 
    

# Encoding works
encoder = MessagePackEncoder(DC)
msgpack_bytes = encoder.encode(DC(inner_dc=InnerDC(a=A(a=1))))

# Decoding fails
decoder = MessagePackDecoder(DC, pre_decoder_func=_default_msgpack_decoder)
python_val = decoder.decode(msgpack_bytes)

assert python_val == DC(inner_dc=InnerDC(a=A(a=1)))
