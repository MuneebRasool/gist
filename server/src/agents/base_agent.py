from langfuse.openai import AsyncOpenAI
from src.config import settings
import json
from src.tools.get_task_deadline import get_task_deadline
from langfuse import Langfuse
from langfuse.decorators import langfuse_context, observe

langfuse = Langfuse()


class BaseAgent:
    """
    Base class for all agents.
    """

    def __init__(
        self,
        model="gpt-4o",
        base_url=settings.LLM_BASE_URL,
        api_key=settings.LLM_API_KEY,
    ):
        self.model = model
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    @observe()
    async def execute(
        self,
        system_prompt: str,
        user_input: str,
        response_format: str = "string",
        tool_schemas=[],
    ) -> str:
        """
        Execute a request to the LLM API

        Args:
            system_prompt: The system prompt
            user_input: The user input prompt
            response_format: The expected response format, either "string" or "json"
            tool_schemas: Optional list of tool schemas for function calling

        Returns:
            The LLM response as a string or JSON object
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                tools=tool_schemas if tool_schemas else None,
                tool_choice="auto" if tool_schemas else None,
                response_format=(
                    {"type": "json_object"} if response_format == "json" else None
                ),
            )

            message = response.choices[0].message

            if hasattr(message, "tool_calls") and message.tool_calls:
                tool_results = []

                for tool_call in message.tool_calls:
                    try:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)

                        tool_result = await self._execute_tool_function(
                            function_name, function_args
                        )

                        tool_results.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": json.dumps(tool_result),
                            }
                        )
                    except Exception as e:
                        tool_results.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": json.dumps({"error": str(e)}),
                            }
                        )

                # Create new messages list with original system prompt, user input and tool results
                new_messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                    {
                        "role": "assistant",
                        "content": message.content or "",
                        "tool_calls": message.tool_calls,
                    },
                    *tool_results,
                ]

                # Call the API again with the tool results
                second_response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=new_messages,
                    response_format=(
                        {"type": "json_object"} if response_format == "json" else None
                    ),
                )

                result = second_response.choices[0].message.content
            else:
                result = message.content

            # Convert JSON string to Python object if response_format is "json"
            if response_format == "json" and result:
                try:
                    return json.loads(result)
                except json.JSONDecodeError as e:
                    return {"error": "Failed to parse API response"}

            return result

        except Exception as e:
            print(f"LLM API error: {str(e)}")
            if response_format == "json":
                return {"error": f"API error: {str(e)}"}
            return f"Error: {str(e)}"

    @observe()
    async def _execute_tool_function(self, function_name, function_args):
        """
        Execute a tool function with the given arguments

        Args:
            function_name: The name of the function to execute
            function_args: The arguments to pass to the function

        Returns:
            The result of the function execution
        """
        if function_name == "get_task_deadline":
            return get_task_deadline(**function_args)
        else:
            raise ValueError(f"Unknown function: {function_name}")
