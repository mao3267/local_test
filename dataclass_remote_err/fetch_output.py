from flytekit.remote.remote import FlyteRemote
from flytekit.configuration import Config
remote = FlyteRemote(
    config=Config.for_endpoint("localhost:30080", True),
)
o = remote.get("flyte://v1/flytesnacks/development/akbdrtkgz8nx9q67nv29/easyexamplet1/o")
# o['o0'] this will fail
print(o)
print(o['o0'])
# task_data = remote.fetch_task(project="flytesnacks", domain="development", name="easy_example.t1",)
# print(task_data)
# print(task_data.interface.outputs['o0'].type) # flytekit.models.types.LiteralType
# We can use `guess_python_type` to convert json schema (stored in the metadata to python types)

# workflow_data = remote.fetch_workflow(project="flytesnacks", domain="development", name="easy_example.wf",)
# print(workflow_data)