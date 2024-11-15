from pydantic import BaseModel
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

class A(BaseModel):
    a: int

class B(BaseModel):
    b: str

@task(container_image=image)
def bar() -> A:
    return A(a=1)

@task(container_image=image)
def foo(inp: Union[A, B]):
    print(inp)

@workflow
def wf():
    v = bar()
    foo(inp=v)

if __name__ == "__main__":
    wf()