from dataclasses import dataclass
from typing import Union, List
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
    a: List[str]
    

@dataclass
class A:
    a: List[int]

@dataclass
class B:
    b: A

@dataclass
class C:
    b: Other

@task(container_image=image)
def parent_task() -> B:
    return B(b=A(a=[1]))

@task(container_image=image)
def my_task(input: Union[C, Other]):
    print(input)

@workflow
def wf():
    p = parent_task()
    my_task(p)

if __name__ == "__main__":
    wf()