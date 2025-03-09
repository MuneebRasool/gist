from openai import AsyncOpenAI
from src.config import settings
from langsmith.wrappers import wrap_openai
import json
class BaseAgent:
    """
    Base class for all agents.
    """
    
    def __init__(
            self, 
            model="gpt-4o-mini",
            base_url= settings.LLM_BASE_URL, 
            api_key= settings.LLM_API_KEY,
    ):
        self.model = model
        self.client = wrap_openai(AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        ))

    async def execute(
        self, 
        system_prompt: str, 
        user_input: str,
        response_format: str = "string",
        tool_schemas=[]
) -> str:
        """
            Makes an LLM call with the given prompt and input.
            Handles tool calling when tool_schemas are provided.
            
            Args:
                system_prompt: The system prompt to provide context
                user_input: The user query or input
                response_format: The desired response format ("string" or "json")
                tool_schemas: List of tool schemas for function calling
                
            Returns:
                The LLM response as a string or JSON object
        """
        print("\n---------------------------------------")
        print(f"🔷 LLM CALL: Model={self.model}, Format={response_format}")
        print(f"🔷 System prompt length: {len(system_prompt)} chars")
        print(f"🔷 User input length: {len(user_input)} chars")
        print(f"🔷 Tool schemas: {len(tool_schemas) if tool_schemas else 0}")
        
        try:
            print("🔷 Sending request to LLM API...")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                tools=tool_schemas if tool_schemas else None,
                tool_choice="auto" if tool_schemas else None,
                response_format={"type": "json_object"} if response_format == "json" else None
            )
            
            print(f"🔷 LLM response received: {len(response.choices[0].message.content) if hasattr(response.choices[0].message, 'content') and response.choices[0].message.content else 'No content'} chars")
            
            message = response.choices[0].message
            
            if hasattr(message, 'tool_calls') and message.tool_calls:
                print(f"🔷 Tool calls detected: {len(message.tool_calls)}")
                tool_results = []
                
                for tool_call in message.tool_calls:
                    try:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        print(f"🔷 Executing tool: {function_name}")
                        tool_result = await self._execute_tool_function(function_name, function_args)
                        
                        tool_results.append({
                            "tool_call_id": tool_call.id,
                            "function_name": function_name,
                            "result": tool_result
                        })
                    except Exception as e:
                        print(f"❌ Tool execution error: {str(e)}")
                        tool_results.append({
                            "tool_call_id": tool_call.id,
                            "error": str(e)
                        })
                
                print("🔷 Sending follow-up request with tool results...")
                follow_up_response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input},
                        message,
                        *[{
                            "role": "tool", 
                            "tool_call_id": result["tool_call_id"],
                            "content": json.dumps(result["result"]) if "result" in result else f"Error: {result['error']}"
                        } for result in tool_results]
                    ],
                    response_format={"type": "json_object"} if response_format == "json" else None
                )
                
                exact_response = follow_up_response.choices[0].message.content
                print(f"🔷 Follow-up response received: {len(exact_response)} chars")
            else:
                exact_response = message.content
            
            if response_format == "json":
                try:
                    print("🔷 Parsing JSON response...")
                    exact_response = exact_response.replace('```json', '').replace('```', '').strip()
                    exact_response = json.loads(exact_response)
                    print("🔷 JSON parsing successful")
                except json.JSONDecodeError as json_err:
                    print(f"❌ JSON parse error: {str(json_err)}")
                    return {}
            
            print("🔷 LLM execution completed successfully")
            print("---------------------------------------\n")
            return exact_response
            
        except Exception as e:
            print(f"❌ LLM execution error: {str(e)}")
            import traceback
            traceback.print_exc()
            print("---------------------------------------\n")
            raise