import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from layers.nlu_primary import nlu_primary
from layers.memory_system import memory_system
from layers.nlu_secondary import nlu_secondary
from layers.nlg_primary import nlg_primary  # Updated NLG with system command execution
from layers.response_refinement import response_refinement
from layers.speak import speak
from layers.self_analyses import executor
app = Flask(__name__)
CORS(app)

# logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def chatbot_pipeline(user_id, text):
    """Processes user input through the chatbot layers and decides on a response."""
    # logging.debug(f"Received input: {text}")
    
    analysis = nlu_primary.analyze(text)  
    refined_analysis = nlu_secondary.refine_analysis(analysis, memory_system.get_stm_context(user_id),memory_system.get_ltm_context)
    memory_system.store_in_stm(user_id, text, refined_analysis)
    #thinking = executor.self_thinking(text, refined_analysis)
    #asigner = executor.assign_handlers(thinking)
    response = nlg_primary.generate_response(text,refined_analysis)  # Handles both chatbot & system commands
    #response = nlg_primary.generate_response(text,asigner)  # Handles both chatbot & system commands
    
    final_response = response_refinement.refine_output(response, text)

    return final_response
    

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot requests from the frontend."""
    data = request.get_json()
    user_text = data.get("text", "").strip()

    if not user_text:
        return jsonify({"error": "No input provided"}), 400

    response = chatbot_pipeline("USER_DEEPANSHU_VISHWAKARMA_1", user_text)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
