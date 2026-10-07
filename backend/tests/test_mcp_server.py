import json
from backend.mcp.server import (
    MCP_PROTOCOL_VERSION,
    create_error_response,
    create_result_response,
    handle_request,
    search_documents,
    handle_message,
)


def test_search_documents_returns_results():
    response=search_documents(
        "python tutorial")

    assert response["query"] == "python tutorial"
    assert response["results"]
    assert response["results"][0]["text"] == (
        "Python programming tutorial for beginners")
    
    
    
def test_create_result_response():
    response=create_result_response(
        1,
        {"status": "ok"},)

    assert response == {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "status": "ok",},}
    
    
    
    
def test_create_error_response():
    response=create_error_response(
        2,
        -32601,
        "Method not found",)

    assert response == {
        "jsonrpc": "2.0",
        "id": 2,
        "error": {
            "code": -32601,
            "message": "Method not found",},}
    
    
    
def test_handle_request_rejects_invalid_version():
    response=handle_request({
        "jsonrpc": "1.0",
        "id": 3,
        "method": "example",})

    assert response["error"]["code"] == -32600
    
    
    
def test_handle_request_rejects_missing_method():
    response=handle_request({
        "jsonrpc": "2.0",
        "id": 4,})

    assert response["error"]["code"] == -32600
    
    
    
def test_handle_request_rejects_unknown_method():
    response=handle_request({
        "jsonrpc": "2.0",
        "id": 5,
        "method": "unknown",})

    assert response["error"]["code"] == -32601
    assert response["id"] == 5
    
    
    
def test_initialize_returns_server_information():
    response=handle_request({
        "jsonrpc": "2.0",
        "id": 6,
        "method":"initialize",
        "params":{
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo":{
                "name": "test-client",
                "version": "1.0.0",},},})

    assert response["id"] == 6
    assert response["result"]["protocolVersion"] == MCP_PROTOCOL_VERSION
    assert response["result"]["serverInfo"]["name"] == (
        "custom-semantic-search-engine")
    assert "tools" in response["result"]["capabilities"]
    
    
    
    
    
def test_tools_list_returns_search_tool():
    response=handle_request({
        "jsonrpc": "2.0",
        "id": 7,
        "method": "tools/list",})

    tools=response["result"]["tools"]

    assert response["id"] == 7
    assert len(tools) == 1
    assert tools[0]["name"] == "search_documents"
    
    
    
    
def test_search_tool_requires_query_string():
    response=handle_request({
        "jsonrpc": "2.0",
        "id": 8,
        "method": "tools/list",})

    tool=response["result"]["tools"][0]
    schema=tool["inputSchema"]

    assert schema["type"] == "object"
    assert schema["required"] == ["query"]
    assert schema["properties"]["query"]["type"] == "string"
    
    
    
def test_tools_call_executes_search():
    response=handle_request({
        "jsonrpc": "2.0",
        "id": 9,
        "method": "tools/call",
        "params": {
            "name": "search_documents",
            "arguments": {
                "query": "python tutorial",},},})

    result=response["result"]
    search_result=result["structuredContent"]

    assert response["id"] == 9
    assert search_result["query"] == "python tutorial"
    assert search_result["results"]
    assert search_result["results"][0]["text"] == (
        "Python programming tutorial for beginners")
    
    
    
    
def test_tools_call_rejects_unknown_tool():
    response=handle_request({
        "jsonrpc": "2.0",
        "id": 10,
        "method": "tools/call",
        "params": {
            "name": "unknown_tool",
            "arguments": {},},})

    assert response["error"]["code"] == -32602
    assert response["error"]["message"] == "Unknown tool"
    
    
    
    
def test_tools_call_requires_arguments():
    response=handle_request({
        "jsonrpc": "2.0",
        "id": 11,
        "method": "tools/call",
        "params": {
            "name": "search_documents",},})

    assert response["error"]["code"] == -32602
    
    
    
    
def test_tools_call_rejects_non_string_query():
    response=handle_request({
        "jsonrpc": "2.0",
        "id": 12,
        "method": "tools/call",
        "params": {
            "name": "search_documents",
            "arguments": {
                "query": 123,},},})

    assert response["error"]["code"] == -32602
    
    
    
    
def test_tools_call_rejects_whitespace_query():
    response=handle_request({
        "jsonrpc": "2.0",
        "id": 13,
        "method": "tools/call",
        "params": {
            "name": "search_documents",
            "arguments": {
                "query": "   ",},},})

    assert response["error"]["code"] == -32602
    
    
    
def test_handle_message_processes_json_request():
    message=json.dumps({
        "jsonrpc": "2.0",
        "id": 14,
        "method": "tools/list",})

    response=json.loads(
        handle_message(message))

    assert response["id"] == 14
    assert response["result"]["tools"][0]["name"] == (
        "search_documents")
    
    
    
def test_handle_message_rejects_invalid_json():
    response=json.loads(
        handle_message("{invalid json"))

    assert response["id"] is None
    assert response["error"]["code"] == -32700
    assert response["error"]["message"] == "Parse error"
    
    
    
def test_initialized_notification_returns_no_response():
    message=json.dumps({
        "jsonrpc": "2.0",
        "method": "notifications/initialized",})

    response=handle_message(message)

    assert response is None
    
    
    
def test_handle_message_rejects_non_object_request():
    response=json.loads(
        handle_message("[]"))

    assert response["id"] is None
    assert response["error"]["code"] == -32600