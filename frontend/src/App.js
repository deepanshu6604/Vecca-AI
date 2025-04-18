import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { motion } from "framer-motion";

export default function Chatbot() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [voiceInput, setVoiceInput] = useState(false);
  const [voiceOutput, setVoiceOutput] = useState(false);
  const chatEndRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:5000/chat", { 
        text: input,
        voice_output: voiceOutput
      });
      
      const botMessage = { text: response.data.response, sender: "bot" };
      setMessages((prev) => [...prev, botMessage]);

      if (voiceOutput) {
        speakResponse(response.data.response);
      }
    } catch (error) {
      console.error("Error fetching response", error);
    }
    setLoading(false);
  };

  const speakResponse = (text) => {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 1;
    window.speechSynthesis.speak(speech);
  };

  const startListening = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Your browser does not support speech recognition.");
      return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event);
    };

    recognition.start();
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="flex h-screen w-full bg-gray-900 text-white items-center justify-center p-8">
      
      <div className="flex w-[90%] h-[90%] space-x-6 rounded-3xl shadow-2xl">
        
        <div className="w-2/5 h-full flex flex-col items-center justify-between p-6 bg-gradient-to-b from-gray-850 to-gray-800 rounded-3xl border border-gray-700 relative">
          
          <div className="absolute inset-0 flex items-center justify-center">
            <img 
              src="/ai-brain.png" 
              alt="AI Brain" 
              className="w-3/4 opacity-10 rounded-2xl"
            />
          </div>

          <h1 className="text-8xl font-extrabold relative z-10 text-blue-400">VECCA</h1>
          <p className="text-md font-medium opacity-75 relative z-10 text-gray-300 mt-auto mb-6">
            Voice Enabled Conversational Cognitive AI
          </p>

          <div className="flex flex-col items-center space-y-6 relative z-10">
            
            <label className="flex items-center space-x-4 p-3 bg-gray-800 rounded-2xl border border-gray-600 w-48 justify-between cursor-pointer">
              <span className="text-lg text-gray-300">Voice Input</span>
              <div 
                className={`w-12 h-6 flex items-center bg-gray-700 rounded-full p-1 transition-all ${
                  voiceInput ? "bg-blue-500" : "bg-gray-600"
                }`}
                onClick={() => setVoiceInput(!voiceInput)}
              >
                <div 
                  className={`w-5 h-5 bg-white rounded-full shadow-md transform transition-all ${
                    voiceInput ? "translate-x-6" : "translate-x-0"
                  }`}
                />
              </div>
            </label>

            <label className="flex items-center space-x-4 p-3 bg-gray-800 rounded-2xl border border-gray-600 w-48 justify-between cursor-pointer">
              <span className="text-lg text-gray-300">Voice Output</span>
              <div 
                className={`w-12 h-6 flex items-center bg-gray-700 rounded-full p-1 transition-all ${
                  voiceOutput ? "bg-blue-500" : "bg-gray-600"
                }`}
                onClick={() => setVoiceOutput(!voiceOutput)}
              >
                <div 
                  className={`w-5 h-5 bg-white rounded-full shadow-md transform transition-all ${
                    voiceOutput ? "translate-x-6" : "translate-x-0"
                  }`}
                />
              </div>
            </label>

          </div>
        </div>

        <div className="w-3/5 h-full flex flex-col p-6 bg-gray-950 text-white rounded-3xl border border-gray-700">
          
          <div className="h-full overflow-y-auto flex flex-col space-y-3 p-4 border border-gray-700 rounded-xl shadow-inner bg-gray-900">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`p-3 rounded-lg w-fit max-w-[80%] ${
                  msg.sender === "user" ? "bg-blue-500 text-white self-end" : "bg-gray-700 text-white self-start"
                }`}
              >
                {msg.text}
              </div>
            ))}
            {loading && (
              <motion.div 
                className="text-gray-400 self-start"
                initial={{ opacity: 0.5 }}
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ repeat: Infinity, duration: 1 }}
              >
                Processing...
              </motion.div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div className="flex mt-4 border-t pt-4">
            <button 
              className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-400 transition-all mr-3"
              onClick={startListening}
            >
              🎙 Start Listening
            </button>
            <input
              type="text"
              className="flex-1 p-3 border rounded-lg focus:outline-none bg-gray-800 text-white placeholder-gray-400"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder="Type your message..."
            />
            <button
              className="ml-3 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-500 transition-all"
              onClick={sendMessage}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
