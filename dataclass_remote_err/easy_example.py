import typing
import os
from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum

from flytekit import task, workflow, ImageSpec

flytekit_hash = "4c73d6be11a6616af5a4cde596f16c96aefbb1cf"
flytekit = f"git+https://github.com/mao3267/flytekit.git@{flytekit_hash}"
image = ImageSpec(
    packages=[flytekit,],
    apt_packages=["git"],
    registry="localhost:30000",
    env={"FLYTE_USE_OLD_DC_FORMAT": "true"},
)

@dataclass
class DC:
    a: int

@task(container_image=image)
def t1(a: int) -> DC:
    return DC(a=a)

@workflow
def wf(a: int) -> DC:
    return t1(a=a)

if __name__ == "__main__":
    from flytekit.clis.sdk_in_container import pyflyte
    from click.testing import CliRunner
    import os
    runner = CliRunner()
    path = os.path.realpath(__file__)

    result = runner.invoke(pyflyte.main, ["run", "--remote", path, "wf","--a", "3"])
    print("Remote Execution: ", result.output)