

from layers.nlu_primary import nlu_primary
from layers.memory_system import memory_system
from layers.nlu_secondary import nlu_secondary
from layers.nlg_primary import nlg_primary  # Updated NLG with system command execution
from layers.response_refinement import response_refinement


'''
def chatbot_pipeline(user_id, text):
    analysis = nlu_primary.analyze("open chrome and open youtube and play any song in it randomly")  
    print("Analysis:",analysis)
    
    
chatbot_pipeline("USER_DEEPANSHU_VISHWAKARMA_1","open chrome and open youtube and play any song in it randomly")

'''
user_id = "USER_DEEPANSHU_VISHWAKARMA_1"
text = "play my favorite song in youtube(sanam teri kasam song)"
analysis = nlu_primary.analyze(text)  

mem = nlu_secondary.refine_analysis(user_id,analysis, memory_system.get_stm_memory(user_id),memory_system.get_ltm_context(user_id))
memory_system.store_in_stm(user_id, text, mem)