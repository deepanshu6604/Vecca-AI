import google.generativeai as genai
from config import GENAI_MODEL_NAME, GENAI_MAX_TOKENS, GENAI_TEMPERATURE


class TaskReasoner:
    def __init__(self):
        self.model = genai.GenerativeModel(GENAI_MODEL_NAME)

    def self_thinking(self, user_input, refined_nlu_data):
        prompt = f"""
        [Self-Thinking Layer]

        🎯 Goal:
        Analyze the user's refined intent and build a task plan:
        - Group related intents.
        - Break them into executable tasks.
        - Identify each task's execution method.

        🧠 Input:
        User Input: {user_input}
        Refined NLU: {refined_nlu_data}

        📤 Output JSON:
        ```json
        {{
            "execution_plan": [
                {{
                    "group": "<group name>",
                    "intents": [
                        {{
                            "intent": "<name>",
                            "method": "internal | external_api | call_input_api",
                            "details": "<extra info>",
                            "prompt_for_user": "<if clarification needed>"
                        }}
                    ]
                }}
            ]
        }}
        ```
        """
        return self._generate(prompt)

    def assign_handlers(self, execution_plan):
        prompt = f"""
        [Execution Assigner Layer]

        🎯 Goal:
        Assign Gemini prompts to each intent in the plan.

        📥 Execution Plan:
        {execution_plan}

        📤 Output JSON:
        ```json
        {{
            "execution_plan": [
                {{
                    "group": "<group name>",
                    "intents": [
                        {{
                            "intent": "<name>",
                            "handler_prompt": "<Gemini instruction>",
                            "output_type": "text | action | data",
                            "acknowledgement_message": "<acknowledgement>"
                        }}
                    ]
                }}
            ]
        }}
        ```
        """
        return self._generate(prompt)

    def execute_tasks(self, assigned_tasks):
        prompt = f"""
        [Task Execution Layer]

        🎯 Goal:
        Perform the task using Gemini prompts, send results as either:
        - Acknowledgement (if action)
        - NLG content (if text)

        📥 Assigned Tasks:
        {assigned_tasks}

        📤 Output JSON:
        ```json
        {{
            "task_results": [
                {{
                    "intent": "<name>",
                    "status": "success | failed",
                    "acknowledgement": "<message>",
                    "final_text_output": "<optional text if needed>"
                }}
            ]
        }}
        ```
        """
        return self._generate(prompt)

    def _generate(self, system_prompt):
        try:
            response = self.model.generate_content(system_prompt, generation_config=genai.GenerationConfig(
                max_output_tokens=GENAI_MAX_TOKENS,
                temperature=GENAI_TEMPERATURE
            ))
            text = response.text.strip() if hasattr(response, "text") else ""
            return text.replace("```json", "").replace("```", "").strip()
        except Exception as e:
            return {"error": f"Gemini API Error: {e}"}


# Instance
executor = TaskReasoner()
