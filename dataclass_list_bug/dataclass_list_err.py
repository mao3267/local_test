from textwrap import shorten

from flytekit import task, workflow
from dataclasses import dataclass
from typing import Any, Dict, Optional, List
from flytekit.core.type_engine import TypeEngine
from dataclasses_json import dataclass_json
from flyteidl.core.execution_pb2 import TaskExecution
from flytekit.core.context_manager import FlyteContextManager
from flytekit.configuration import SerializationSettings
from flytekit.core.base_task import PythonTask
from flytekit.core.interface import Interface
from flytekit.extend.backend.base_agent import (
    AgentRegistry,
    Resource,
    SyncAgentBase,
    SyncAgentExecutorMixin,
)
from flytekit.models.literals import LiteralMap
from flytekit.models.task import TaskTemplate


@dataclass_json
@dataclass
class Foo:
    val: str


class FooAgent(SyncAgentBase):
    def __init__(self) -> None:
        super().__init__(task_type_name="foo")

    def do(
        self,
        task_template: TaskTemplate,
        inputs: Optional[LiteralMap] = None,
        **kwargs: Any,
    ) -> Resource:
        return Resource(
            phase=TaskExecution.SUCCEEDED, outputs={"foos": [Foo(val="a"), Foo(val="b")], "has_foos": True}
        )


AgentRegistry.register(FooAgent())


class FooTask(SyncAgentExecutorMixin, PythonTask):  # type: ignore
    _TASK_TYPE = "foo"

    def __init__(self, name: str, **kwargs: Any) -> None:
        task_config: dict[str, Any] = {}

        outputs = {"has_foos": bool, "foos": Optional[List[Foo]]}

        super().__init__(
            task_type=self._TASK_TYPE,
            name=name,
            task_config=task_config,
            interface=Interface(outputs=outputs),
            **kwargs,
        )

    def get_custom(self, settings: SerializationSettings) -> Dict[str, Any]:
        return {}


foo_task = FooTask(name="foo_task")


@task
def foos_task(foos: list[Foo]) -> None:
    print(f"hi {foos}")


@workflow
def dc_wf(foos: list[Foo] = [Foo(val="a"), Foo(val="b")]) -> None:
    has_foos, foos = foo_task()
    foos_task(foos=foos)


if __name__ == "__main__":
    dc_wf([Foo(val="a"), Foo(val="b")])
