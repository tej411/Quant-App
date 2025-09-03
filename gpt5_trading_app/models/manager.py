from dataclasses import dataclass
from typing import Dict, Callable
@dataclass
class AlgoInfo:
    key: str
    name: str
    family: str
    create_fn: Callable
ALGOS: Dict[str, AlgoInfo] = {}
def register_algo(info: AlgoInfo): ALGOS[info.key] = info
def list_algos(): return {k: (v.name, v.family) for k, v in ALGOS.items()}
