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

        message = response.choices[0].message
        
        if hasattr(message, 'tool_calls') and message.tool_calls:
            tool_results = []
            
            for tool_call in message.tool_calls:
                try:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    tool_result = await self._execute_tool_function(function_name, function_args)
                    
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "function_name": function_name,
                        "result": tool_result
                    })
                except Exception as e:
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "error": str(e)
                    })
            
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
        else:
            exact_response = message.content
        
        if response_format == "json":
            try:
                exact_response = exact_response.replace('```json', '').replace('```', '').strip()
                exact_response = json.loads(exact_response)
                return exact_response
            except json.JSONDecodeError:
                return {}
        
        return exact_response