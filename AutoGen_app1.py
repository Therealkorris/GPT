import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

config_list = [
    {
        "api_type": "open_ai",
        "api_base": "http://localhost:1234/v1",
        "api_key": 'NULL'
    },
]

llm_config={
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

# create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="You are a text summarization assistant.",
    llm_config=llm_config
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satifaction. 
    Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task = """
Read file Test.txt in work_dir and write a story about the content.
"""


# the assistant receives a message from the user_proxy, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message=task
)
