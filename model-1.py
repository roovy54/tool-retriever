# Importing necessary libraries and modules
from langchain_groq import ChatGroq  # For interacting with the Groq API
from dotenv import load_dotenv  # For loading environment variables
from toolset import tools  # Importing toolset for tool information
from tools_context import tool_descriptions_context  # Context for tool descriptions
from examples_proto import ExampleRetriever, bge  # For retrieving examples
import json  # For handling JSON data
import os  # For interacting with the operating system
from prompt_templates import (
    CoT_prompt_template,
    ToT_prompt_template,
)  # Templates for CoT and ToT prompting styles
from tools_proto import ToolsetBM25Encoder  # Encoder for toolset BM25
import gradio as gr  # For creating a Gradio interface

# Load environment variables
load_dotenv()

# Setting up the Groq API key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initializing the Groq LLM
llm = ChatGroq(model_name="llama-3.1-8b-instant")

# Creating an instance of the Examples Retriever
example_retriever = ExampleRetriever(
    bge(),
)


# Function to process the query
def process_query(query, tools, prompting_style):
    # Retrieve examples
    examples = example_retriever.retrieve(query, k=5)

    # Initialize encoder
    encoder = ToolsetBM25Encoder()

    # Encode tools
    encoder.encode_tools(tools)

    # Retrieve top 5 tools
    tools_retrieved = encoder.search(query, top_k=5)

    # Extract just the tool information from the results
    top_5_tools = [result["tool"] for result in tools_retrieved]

    # Convert tools and examples to string representations
    tools_str = json.dumps(top_5_tools, indent=2)
    examples_str = str(examples)

    if prompting_style == "CoT":
        # Use the combined CoT template
        cot_chain = CoT_prompt_template | llm
        result = cot_chain.invoke(
            input={
                "query": query,
                "tools_context": tool_descriptions_context,
                "tools": tools_str,
                "examples": examples_str,
            }
        )

        # Parse the result
        try:
            result_dict = json.loads(result.content)
            output = result_dict["output"]
            reasoning = "\n".join(result_dict["reasoning"])  # Convert list to string
        except json.JSONDecodeError:
            # If the result is not valid JSON, return an error
            output = []
            reasoning = "Error: Invalid JSON output"

    elif prompting_style == "ToT":
        tot_chain = ToT_prompt_template | llm
        result = tot_chain.invoke(
            input={
                "query": query,
                "tools_context": tool_descriptions_context,
                "tools": tools_str,
                "examples": examples_str,
            }
        )

        # Parse the result
        try:
            result_dict = json.loads(result.content)
            output = result_dict["output"]
            thought_tree = json.dumps(result_dict["thought_tree"], indent=2)
            selected_path = json.dumps(result_dict["selected_path"], indent=2)
            reasoning = (
                f"Thought Tree:\n{thought_tree}\n\nSelected Path:\n{selected_path}"
            )
        except json.JSONDecodeError:
            # If the result is not valid JSON, return an error
            output = []
            reasoning = "Error: Invalid JSON output"

    return output, reasoning, examples


# Gradio interface function
def gradio_interface(query, prompting_style):
    output, reasoning, examples = process_query(query, tools, prompting_style)

    # Save output to file
    with open("output.json", "w") as json_file:
        json.dump(output, json_file, indent=2)

    # Save reasoning to file
    with open("reasoning.txt", "w") as reasoning_file:
        reasoning_file.write(reasoning)

    return output, reasoning


# Create Gradio interface with prompting style selection
iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter your query here..."),
        gr.Radio(["CoT", "ToT"], label="Prompting Style", value="CoT"),
    ],
    outputs=[gr.JSON(label="Output"), gr.Textbox(label="Reasoning", lines=10)],
    title="Tool Retriever",
    description="Process queries using CoT or ToT prompting styles.",
)

# Launch the interface
iface.launch()
