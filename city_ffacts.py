import yaml
from julep import Julep
import time

# Initialize the client
client = Julep(api_key=JULEP_API_KEY)  # Replace with your actual API key

# Use your existing agent ID here
agent_id = AGENT_ID  # Replace with your City Facts agent ID

# Load YAML task definition
with open("city_facts_task.yaml", "r") as f:
    task_definition = yaml.safe_load(f)

task = client.tasks.create(
    agent_id,
    name=task_definition["name"],
    description=task_definition["description"],
    tools=task_definition["tools"],
    main=task_definition["main"]
)

# Create execution for the task
execution = client.executions.create(
    task.id,
    input={
        "cities": ["Tokyo", "Barcelona", "Cairo"]
    }
)

# Poll for the result until completion
while True:
    result = client.executions.get(execution.id)
    if result.status in ("succeeded", "failed"):
        break
    print(f"Status: {result.status}")
    time.sleep(2)

# Print the final output or error
if result.status == "succeeded":
    print("✅ OUTPUT:\n", result.output)
else:
    print("❌ ERROR:\n", result.error)