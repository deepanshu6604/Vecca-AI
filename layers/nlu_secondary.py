import google.generativeai as genai
from config import GENAI_MODEL_NAME, GENAI_MAX_TOKENS, GENAI_TEMPERATURE

class NLUSecondary:
    def __init__(self):
        self.model = genai.GenerativeModel(GENAI_MODEL_NAME)

    def refine_analysis(self, user_id, nlu_primary_analysis, stm_context, ltm_context):
        """
        Refines insights (intent, emotion, context, etc.) from NLU Primary.
        Uses STM first, LTM only if STM is insufficient, else falls back to primary input.
        """
        system_prompt = f"""
        You are an advanced NLU module responsible for **refining previously extracted analysis**
        using recent session (STM) and long-term memory (LTM) only for **supportive insights**.

        Do NOT mix up the refinement task with memory tasks. Only use STM/LTM to **support** your reasoning. 
        If STM is insufficient, then check LTM. If both are unavailable or unhelpful, fall back to only the primary analysis.

        🎯 Refine this:
        - Intents (can be multiple)
        - Emotion
        - Tone
        - User context & description
        - Maintain structure and clarity, especially for multi-intent input.

        🧠 Memory:
        STM (current session): {stm_context}
        LTM (historical context): {ltm_context}

        🔍 Primary Analysis (from NLU Primary):
        {nlu_primary_analysis}

        ✨ Return this strict JSON:
        ```json
        {{
            "refined_emotion": "frustrated | neutral | happy | etc.",
            "refined_intents": [
                {{
                    "intent": "intent_name",
                    "confidence": 0.9,
                    "priority": 1,
                    "entities": [{{"entity": "value", "type": "type"}}],
                    "negated": false
                }}
            ],
            "refined_tone": "formal | casual | excited | etc.",
            "is_sarcastic": true | false,
            "is_ironic": true | false,
            "is_negated": true | false,
            "is_confused": true | false,
            "clarification_required": true | false,
            "coreference_resolved_input": "Resolved version of user input",
            "language_level": "simple | moderate | complex",
            "disfluencies_detected": true | false,
            "refined_context": "task | scheduling | feedback | etc.",
            "refined_description": "Improved version of what the user wanted",
            "factual_memory_extract": [
                {{
                    "statement": "I live in Delhi",
                    "type": "location",
                    "source": "refined_input"
                }}
            ]
        }}
        ```
        """

        try:
            response = self.model.generate_content(system_prompt, generation_config=genai.GenerationConfig(
                max_output_tokens=GENAI_MAX_TOKENS,
                temperature=GENAI_TEMPERATURE,
            ))
            response_text = response.text.strip() if hasattr(response, "text") else ""
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            return response_text

        except Exception as e:
            return {"error": f"NLU Secondary Error: {e}"}

    def feedback_analyser(self, user_id, user_feedback):
        """
        Analyzes user feedback from NLU Primary to detect which system layer(s) need improvement.
        Only the feedback text is used for tagging.
        """
        system_prompt = f"""
        **[Feedback Analyzer Layer]**

        🎯 Task:
        Analyze the user feedback text and determine which internal layer(s) require improvement.

        ✅ Use only the statement below:
        "{user_feedback}"

        🧠 Possible system layers to tag:
        - "nlu_primary"
        - "nlu_secondary"
        - "nlg_primary"
        - "nlg_secondary"
        - "stm_to_ltm"
        - "stm_to_factual_memory"
        - "self_thinking_layer"
        - "text_to_voice_layer"
        - "voice_to_text_layer"

        🚦 Return this strict JSON:
        ```json
        {{
            "detected_feedback": true | false,
            "summary": "What user meant",
            "layer_tags": ["layer1", "layer2"],
            "suggestion": "Optional fix or improvement if clear"
        }}
        ```
        - If feedback is unclear, return `detected_feedback: false`.
        - Keep reasoning focused and structured.
        """

        try:
            response = self.model.generate_content(system_prompt, generation_config=genai.GenerationConfig(
                max_output_tokens=GENAI_MAX_TOKENS,
                temperature=GENAI_TEMPERATURE,
            ))
            response_text = response.text.strip() if hasattr(response, "text") else ""
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            return response_text

        except Exception as e:
            return {"error": f"Feedback Analyzer Error: {e}"}
'''
    def factual_extract(self, user_id, input_text):
        
        try:
            response = self.model.generate_content(system_prompt, generation_config=genai.GenerationConfig(
                max_output_tokens=GENAI_MAX_TOKENS,
                temperature=GENAI_TEMPERATURE,
            ))
            response_text = response.text.strip() if hasattr(response, "text") else ""
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            return response_text

        except Exception as e:
            return {"error": f"Feedback Analyzer Error: {e}"}
'''
# Instance
nlu_secondary = NLUSecondary()
