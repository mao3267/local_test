from dataclasses import dataclass
from typing import Union
from flytekit import task, workflow
from flytekit.image_spec import ImageSpec


flytekit_hash = "3475ddc41f2ba31d23dd072362be704d7c2470a0"
flytekit = f"git+https://github.com/flyteorg/flytekit.git@{flytekit_hash}"

# Define custom image for the task
image = ImageSpec(
    packages=[
                flytekit,
                "pydantic>2",
                "pandas",
                "pyarrow"
],
    apt_packages=["git"],
    registry="localhost:30000",
    builder="default",
)

@dataclass
class Other:
    c: str


@dataclass
class LeafBase():
    leaf: int

@dataclass
class Leaf(LeafBase):
    other: int

@dataclass
class Parent:
    l: LeafBase

@task(container_image=image)
def parent_task() -> Parent:
    return Parent(l=Leaf(leaf=1, other=2))

@task(container_image=image)
def my_task(input: Union[Parent, Other]):
    print(input)

@workflow
def wf():
    p = parent_task()
    my_task(p)

if __name__ == "__main__":
    wf()