from langchain_groq import ChatGroq
from dotenv import load_dotenv
from toolset import tools
import json
import os
from prompt_templates import (
    CoT_prompt_template,
    ToT_prompt_template,
)  # Import the new template
import gradio as gr

load_dotenv()

# Set up the Groq API key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the Groq LLM
llm = ChatGroq(model_name="llama-3.1-8b-instant")

# Examples
examples = ""


# Function to process the query
def process_query(query, tools, examples, prompting_style):
    # Convert tools and examples to string representations
    tools_str = json.dumps(tools, indent=2)
    examples_str = examples

    # Create the LLMChain based on the selected prompting style
    if prompting_style == "CoT":
        chain = CoT_prompt_template | llm
    elif prompting_style == "ToT":
        chain = ToT_prompt_template | llm

    # Run the chain using the new method
    result = chain.invoke(
        input={
            "query": query,
            "tools": tools_str,
            "examples": examples_str,
        }
    )

    # Parse the result
    result_dict = json.loads(result.content)
    output = result_dict["output"]

    if prompting_style == "CoT":
        reasoning = "\n".join(result_dict["reasoning"])
    elif prompting_style == "ToT":
        reasoning = json.dumps(result_dict["thought_tree"], indent=2)

    return output, reasoning


# Gradio interface function
def gradio_interface(query, prompting_style):
    output, reasoning = process_query(query, tools, examples, prompting_style)

    # Save output to file
    with open("output.json", "w") as json_file:
        json.dump(output, json_file, indent=2)

    # Save reasoning to file
    if prompting_style == "CoT":
        with open("reasoning.txt", "w") as reasoning_file:
            reasoning_file.write(reasoning)
    elif prompting_style == "ToT":
        with open("reasoning.json", "w") as reasoning_file:
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
