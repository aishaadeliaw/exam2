import streamlit as st
import openai
import json
from dotenv import load_dotenv
from utilities.chroma import query_chroma_collection

load_dotenv()

def agent_with_search(investigation_collection, objective, input_list):

    # st.write(f"Agent is now running with objective: {objective}")

    # 1. Define a list of callable tools for the model
    tools = [
        {
            "type": "function",
            "name": "query_chroma_collection",
            "description": """Perform a semantic vector-based query against the ChromaDB vector database
            to find compliance checklist for a corporation.
            Do not stop until you have found all relevant information.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A semantic vector-based query that will be used to perform the search in the vector database.",
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "The number of results that you want returned from the vector database.",
                    },
                },
                "required": ["query", "n_results"],
            },
        },
    ]

    # 2. Prompt the model with tools defined
    response = openai.responses.create(
        model="gpt-5",
        tools=tools,
        input=input_list,
    )

    # Save function call outputs for subsequent requests
    input_list += response.output

    # st.write(f"Response Output: {response.output}")

    for item in response.output:
        if item.type == "function_call":
            if item.name == "query_chroma_collection":
                st.write(f"Agent has decided to use the ChromaDB search.")

                # 3. Execute function logic for agent_with_search
                arguments = json.loads(item.arguments)
                documents = query_chroma_collection(
                    collection=investigation_collection, 
                    query=arguments.get("query"),
                    n_results=arguments.get("n_results"),
                )
                # st.write(f"ChromaDB search returned: {documents.get("metadatas")}")
                
                # 4. Provide function call results to the model
                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                    "documents": documents
                    })
                })

    response = openai.responses.create(
        model="gpt-5",
        instructions=f"""Your objective is: {objective}.
        If you think your objective has been completed, you must state 'FINISHED'.
        Alternatively, if you think there are more lines of inquiry that
        you should investigate with further document searches, respond 'CONTINUE'.""",
        tools=tools,
        input=input_list,
    )

    if "FINISHED" in response.output_text:
        input_list.append({
            "role": "assistant",
            "content": [{"type": "output_text", "text": "FINISHED"}]
        })
    
    else:
        input_list.append({
            "role": "assistant",
            "content": [{"type": "output_text", "text": "CONTINUE"}]
        })

    return input_list