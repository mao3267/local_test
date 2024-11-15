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
class Parent:
    a: int

@dataclass
class Child(Parent):
    b: int = 1

@dataclass
class Other:
    c: str

@task(container_image=image)
def foo() -> Parent:
    return Parent(a=1)

@task(container_image=image)
def my_task(input: Union[Child, Other]):
    print(input)

@workflow
def wf():
    a = foo()
    my_task(a)

if __name__ == "__main__":
    wf()