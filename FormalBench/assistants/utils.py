from langchain_core.messages.base import BaseMessage
from langchain_core.messages.human import HumanMessage
from .state import State


def save_workflow_to_image(workflow, filename: str):
    try:
        # Generate the image data
        image_data = workflow.get_graph().draw_mermaid_png()

        # Save the image data to a file
        with open(filename, "wb") as f:
            f.write(image_data)

        print(f"Image saved successfully as {filename}")
    except Exception as e:
        # Print the error if it occurs
        print(f"An error occurred: {e}")


def _print_event(event: dict, _printed: set, max_length=1500):
    messages = event.get("messages")
    for message in messages:
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)

    curr_spec = event.get("curr_spec")
    n_iters = event.get("n_iters")
    if curr_spec:
        print(
            f"================================ Generated Sepecification - Iter {n_iters} ================================="
        )
        print(curr_spec)

    analysis_results = event.get("analysis_results")
    if analysis_results:
        print("Iteration: ", n_iters)
        print(
            "================================ Analysis Results ================================="
        )
        print("Number of errors: ", analysis_results[-1][0])
        print("Output: ", analysis_results[-1][1])


def update_messages(state: State, new_message: BaseMessage) -> State:
    messages = state["messages"] + [new_message]
    return {**state, "messages": messages}
