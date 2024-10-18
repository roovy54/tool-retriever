# Importing necessary libraries
import json  # For handling JSON data
from rank_bm25 import BM25Okapi  # For BM25 ranking
from sentence_transformers import SentenceTransformer  # For sentence embeddings
import numpy as np  # For numerical computations
import faiss  # For similarity search
from collections import defaultdict  # For creating default dictionaries
from typing import List, Dict, Any  # For type hinting


# Defining the ToolsetBM25Encoder class
class ToolsetBM25Encoder:
    def __init__(self):
        # Initializing dictionaries to store BM25 encoders and tool index
        self.bm25_encoders = {}
        self.tool_index = {}
        # Defining field weights for different aspects of tools
        self.field_weights = {
            "tool_name": 3.0,  # Higher weight for exact tool name matches
            "description": 2.0,  # Important for understanding tool purpose
            "args": 1.5,  # Arguments are moderately important
            "arg_description": 1.0,  # Arg descriptions help in understanding
            "output": 1.0,  # Output is least important for matching
        }

    # Method to preprocess text by tokenizing and removing special characters
    def _preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text by tokenizing and removing special characters
        """
        # Convert to lowercase and split
        tokens = text.lower().split()
        # Remove special characters and normalize
        tokens = [token.strip('.,()[]{}") ') for token in tokens]
        # Remove empty tokens
        return [token for token in tokens if token]

    # Method to encode arguments with improved structure
    def _encode_args(self, args: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Encode arguments with improved structure
        """
        arg_tokens = {"names": [], "types": [], "descriptions": [], "metadata": []}

        for arg in args:
            # Encode arg name
            arg_tokens["names"].extend(self._preprocess_text(arg["arg_name"]))

            # Encode arg type with array indicator
            arg_type = (
                f"{arg['arg_type']}_array" if arg.get("is_array") else arg["arg_type"]
            )
            arg_tokens["types"].extend(self._preprocess_text(arg_type))

            # Encode arg description if available
            if "arg_description" in arg:
                arg_tokens["descriptions"].extend(
                    self._preprocess_text(arg["arg_description"])
                )

            # Encode metadata (required/optional, array/single)
            metadata = []
            if arg.get("is_required"):
                metadata.append("required")
            else:
                metadata.append("optional")
            if arg.get("is_array"):
                metadata.append("array")
            else:
                metadata.append("single")
            arg_tokens["metadata"].extend(metadata)

        return arg_tokens

    # Method to encode output information
    def _encode_output(self, output: Dict[str, Any]) -> List[str]:
        """
        Encode output information
        """
        output_tokens = []
        output_tokens.extend(self._preprocess_text(output["arg_type"]))
        if output.get("is_array"):
            output_tokens.append("array")
        if output.get("is_required"):
            output_tokens.append("required")
        return output_tokens

    # Method to encode the entire toolset using separate BM25 encoders for different aspects
    def encode_tools(self, tools_json: str):
        """
        Encode the entire toolset using separate BM25 encoders for different aspects
        """
        tools = tools_json

        # Initialize storage for different aspects of tools
        tool_docs = defaultdict(list)

        for idx, tool in enumerate(tools):
            # Store tool index
            self.tool_index[idx] = tool

            # Encode tool name and description
            tool_docs["name"].append(self._preprocess_text(tool["tool_name"]))
            tool_docs["description"].append(
                self._preprocess_text(tool["tool_description"])
            )

            # Encode arguments
            arg_tokens = self._encode_args(tool["args"])
            for key, tokens in arg_tokens.items():
                tool_docs[f"args_{key}"].append(tokens)

            # Encode output
            tool_docs["output"].append(self._encode_output(tool["output"]))

        # Create BM25 encoders for each aspect
        for aspect, docs in tool_docs.items():
            self.bm25_encoders[aspect] = BM25Okapi(docs)

    # Method to search tools using weighted BM25 scores across different aspects
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search tools using weighted BM25 scores across different aspects
        """
        query_tokens = self._preprocess_text(query)

        # Calculate scores for each aspect
        scores = np.zeros(len(self.tool_index))

        for aspect, encoder in self.bm25_encoders.items():
            # Get base weight for this aspect
            base_weight = self.field_weights.get(aspect.split("_")[0], 1.0)

            # Calculate scores for this aspect
            aspect_scores = encoder.get_scores(query_tokens)

            # Apply weight and add to total scores
            scores += aspect_scores * base_weight

        # Get top-k tools
        top_indices = np.argsort(scores)[-top_k:][::-1]

        # Return tools with their scores
        results = []
        for idx in top_indices:
            if scores[idx] > 0:  # Only return results with positive scores
                results.append(
                    {"tool": self.tool_index[idx], "score": float(scores[idx])}
                )

        return results
