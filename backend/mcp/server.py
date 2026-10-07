import json
import sys

from backend.data.documents import DOCUMENTS
from backend.models.query import Query
from backend.services.search.search_engine import SearchEngine

MCP_PROTOCOL_VERSION="2025-11-25"
SERVER_NAME="custom-semantic-search-engine"
SERVER_VERSION="1.0.0"
search_engine=SearchEngine(DOCUMENTS)


def search_documents(query_text):
    query=Query(query_text)

    _, results=search_engine.search(query)

    return {
        "query": query_text,
        "results": results,}
    
    
    
def create_result_response(request_id, result):
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result,}
    
    
def create_error_response(request_id, code, message):
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message, },}
    



def handle_initialize(request_id):
    result={
        "protocolVersion": MCP_PROTOCOL_VERSION,
        "capabilities": {
            "tools": {},
        },
        "serverInfo": {
            "name": SERVER_NAME,
            "version": SERVER_VERSION,},}

    return create_result_response(
        request_id,
        result,)
    
    
    
    
def handle_tools_list(request_id):
    result={
        "tools":[
            {
                "name": "search_documents",
                "description":(
                    "Search documents using the custom semantic search engine."
                ),
                "inputSchema":{
                    "type": "object",
                    "properties":{
                        "query":{
                            "type": "string",
                            "description": "The search query.",
                        },
                    },
                    "required": ["query"],}, }, ],}

    return create_result_response(
        request_id,
        result,)
    
    


def handle_tools_call(request_id, params):
    if not isinstance(params, dict):
        return create_error_response(
            request_id,
            -32602,
            "Invalid params",)

    tool_name=params.get("name")
    arguments=params.get("arguments")

    if tool_name != "search_documents":
        return create_error_response(
            request_id,
            -32602,
            "Unknown tool",)

    if not isinstance(arguments, dict):
        return create_error_response(
            request_id,
            -32602,
            "Invalid params",)

    query_text=arguments.get("query")

    if not isinstance(query_text, str) or not query_text.strip():
        return create_error_response(
            request_id,
            -32602,
            "Invalid query",)

    search_result=search_documents(query_text)

    result={
        "content": [
            {
                "type": "text",
                "text": (
                    f"Search completed for: {search_result['query']}"
                ),
            },
        ],
        "structuredContent": search_result,}

    return create_result_response(
        request_id,
        result,)
    
    
    
    
    
def handle_request(request):
    request_id=request.get("id")
    
    if request.get("jsonrpc") != "2.0":
        return create_error_response(
            request_id,
            -32600,
            "Invalid Request",)

    method=request.get("method")

    if not isinstance(method, str):
        return create_error_response(
            request_id,
            -32600,
            "Invalid Request",)
        
    if method == "notifications/initialized":
        return None    
    
    
    if method == "initialize":
        return handle_initialize(request_id)
    
    if method == "tools/list":
        return handle_tools_list(request_id)
    
    
    if method == "tools/call":
        return handle_tools_call(
            request_id,
            request.get("params"),)

    return create_error_response(
        request_id,
        -32601,
        "Method not found",)
    
    
    
    
    
def handle_message(message):
    try:
        request=json.loads(message)
    except json.JSONDecodeError:
        response=create_error_response(
            None,
            -32700,
            "Parse error",)
        return json.dumps(response)
    
    if not isinstance(request, dict):
        response=create_error_response(
            None,
            -32600,
            "Invalid Request",)

        return json.dumps(response)
    

    response=handle_request(request)
    if response is None:
            return None

    return json.dumps(response)



def run_server():
    for line in sys.stdin:
        message=line.strip()
        if not message:
            continue
        
        response=handle_message(message)

        if response is None:
            continue

        sys.stdout.write(response + "\n")
        sys.stdout.flush()
        
        
        
        
if __name__ == "__main__":
    run_server()
    
    
    