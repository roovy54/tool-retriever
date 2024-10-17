from langchain.prompts import PromptTemplate

# Define the cot prompt template
CoT_prompt_template = PromptTemplate(
    input_variables=["query", "tools", "examples"],
    template="""
You are an AI assistant tasked with determining the appropriate tools and their arguments to solve a given query. You have access to a set of tools and example use cases. Please analyze the query and provide a step-by-step reasoning to determine which tools to use and how to use them.

Query: {query}

Available Tools:
{tools}

Example Use Cases:
{examples}

Please think through this step-by-step and provide your response strictly in the following JSON format without any additional text:

{{
  "reasoning": [
    "1. Analyze the query and identify the key requirements.",
    "2. Review the available tools and their descriptions.",
    "3. Consider the example use cases for guidance if present.",
    "4. Determine which tools are necessary to fulfill the query.",
    "5. For each selected tool, identify the required arguments based on the query."
  ],
  "output": [
    {{
      "tool_name": "tool_name_here",
      "arguments": [
        {{
          "argument_name": "arg_name_here",
          "argument_value": "arg_value_here"
        }}
      ]
    }}
  ]
}}

Important notes:
1. If you need to use the output of a previous tool as input for another tool, use the format "$$PREV[i]", where i is the index of the previous tool (0-based). Example: if there was a need to use the first tool it is "$$PREV[0]"
2. If the query cannot be solved using existing tools, provide an empty JSON object as the output: {{"output": []}}.
3. Focus only on solving what is explicitly given in the query. Do not add extra steps or solve anything not directly requested.

Ensure that your response is a valid JSON object with "reasoning" and "output" keys, and nothing else.
""",
)

# Define the tot prompt template
ToT_prompt_template = PromptTemplate(
    input_variables=["query", "tools", "examples"],
    template="""
You are an AI assistant using the Tree of Thoughts strategy to solve queries with available tools. Analyze the query, generate multiple thought branches, evaluate them, and select the most promising path.

Query: {query}

Available Tools:
{tools}

Example Use Cases:
{examples}

Please provide your response in the following JSON format without any additional text:

{{
  "thought_tree": [
    {{
      "branch": 1,
      "thoughts": [
        "1. Initial thought for branch 1",
        "2. Subsequent thought",
        "3. Final thought for this branch"
      ],
      "evaluation": "Evaluation of branch 1's potential"
    }},
    {{
      "branch": 2,
      "thoughts": [
        "1. Initial thought for branch 2",
        "2. Subsequent thought",
        "3. Final thought for this branch"
      ],
      "evaluation": "Evaluation of branch 2's potential"
    }},
    {{
      "branch": 3,
      "thoughts": [
        "1. Initial thought for branch 3",
        "2. Subsequent thought",
        "3. Final thought for this branch"
      ],
      "evaluation": "Evaluation of branch 3's potential"
    }}
  ],
  "selected_path": {{
    "branch": "Number of the selected branch",
    "reasoning": "Explanation for why this branch was selected"
  }},
  "output": [
    {{
      "tool_name": "tool_name_here",
      "arguments": [
        {{
          "argument_name": "arg_name_here",
          "argument_value": "arg_value_here"
        }}
      ]
    }}
  ]
}}

Important notes:
1. If you need to use the output of a previous tool as input for another tool, use the format "$$PREV[i]", where i is the index of the previous tool (0-based).
2. If the query cannot be solved using existing tools, provide an empty JSON array as the output: {{"output": []}}.
3. Focus only on solving what is explicitly given in the query. Do not add extra steps or solve anything not directly requested.

Ensure that your response is a valid JSON object with "thought_tree", "selected_path", and "output" keys, and nothing else.
""",
)
