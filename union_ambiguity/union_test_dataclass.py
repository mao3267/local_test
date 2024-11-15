from dataclasses import dataclass
from typing import Optional, Union
from flytekit import task, workflow
from jsonA import D as pydanticD
from jsonA import A as pydanticA
from flytekit.image_spec import ImageSpec
from flytekit.types.file import FlyteFile
from pydantic import BaseModel

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

# @dataclass 
# class Parent:
#     a: int

# @dataclass
# class Child(Parent):
#     a: int

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


# @task(container_image=image)
# def foo() -> Child:
#     return Child(a=1, b=2)

@task(container_image=image)
def parent_task() -> Parent:
    return Parent(l=Other(c="hello"))

@task(container_image=image)
def my_task(input: Union[Parent, Other]):
    print(input)

@workflow
def wf():
    # a = foo()
    # my_task(a)
    p = parent_task()
    my_task(p)

if __name__ == "__main__":
    wf()