import { useNavigate } from 'react-router-dom';
import { Mic, PhoneOff, Settings, Volume2 } from 'lucide-react';
import { ScribbleMark, Sparkle } from '../components/Doodles';
import { useEffect, useRef, useState } from 'react';

export default function Interview() {
  const navigate = useNavigate();

  // Array of finalized messages: { type: "user_final" | "ai_message", text: "..." }
  const [messages, setMessages] = useState([]);

  // Ref for auto-scrolling chat
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Refs to keep track of our connections
  const wsRef = useRef(null);
  const mediaRecorderRef = useRef(null);

  useEffect(() => {
    // 1. Connect to your FastAPI WebSocket
    const sessionId = "65e0d405-0728-4bfa-b5b4-6a1b51d95cd4";
    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/interview/${sessionId}`);
    wsRef.current = ws;

    ws.onopen = async () => {
      console.log("Connected to Backend WebSocket!");

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // 1. Create an AudioContext at exactly 16kHz (what most STT models want)
        const audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
        const source = audioContext.createMediaStreamSource(stream);

        // 2. Create a script processor to grab raw audio chunks
        const processor = audioContext.createScriptProcessor(4096, 1, 1);

        source.connect(processor);
        processor.connect(audioContext.destination);

        // 3. Every time a chunk of raw audio is ready...
        processor.onaudioprocess = (e) => {
          if (ws.readyState === WebSocket.OPEN) {
            // Get raw Float32 soundwaves
            const float32Array = e.inputBuffer.getChannelData(0);

            // Convert to 16-bit PCM (Int16) which is the industry standard for STT
            const int16Array = new Int16Array(float32Array.length);
            for (let i = 0; i < float32Array.length; i++) {
              int16Array[i] = Math.max(-1, Math.min(1, float32Array[i])) * 0x7FFF;
            }

            // Send the raw PCM bytes to FastAPI!
            ws.send(int16Array.buffer);
          }
        };

        // Save refs so we can clean them up later
        mediaRecorderRef.current = { stream, audioContext, processor };

      } catch (err) {
        console.error("Microphone access denied:", err);
      }

    };

    // 5. When the backend sends us finalized text (user or AI), display it!
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "user_final" || data.type === "ai_message") {
          setMessages(prev => [...prev, data]);
        }
      } catch (e) {
        // If it's not JSON (like the old raw string), ignore it or log it
      }
    };

    ws.onclose = () => console.log("WebSocket Disconnected");

    // Cleanup when the user leaves the page
    return () => {
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.processor.disconnect();
        mediaRecorderRef.current.audioContext.close();
        mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      }
      if (ws.readyState === WebSocket.OPEN) ws.close();
    };

  }, []);

  return (
    <div className="fixed inset-0 bg-white flex flex-col p-6 z-50 overflow-hidden font-body text-saas-ink">

      {/* Header */}
      <div className="w-full flex justify-between items-center px-4 py-3 mb-4">
        <h1 className="text-2xl font-brand font-extrabold text-saas-ink tracking-tight flex items-center gap-2">
          Coach<span className="text-saas-amber">.ai</span>
        </h1>
        <div className="flex items-center gap-3 bg-saas-peach px-5 py-2 rounded-xl shadow-sm">
          <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
          <span className="font-bold text-xs">Recording • 00:00</span>
        </div>
      </div>

      {/* Main Layout Area */}
      <div className="flex-1 min-h-0 w-full max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6 relative">

        {/* Main Caller Tile (The Coach) */}
        <div className="lg:col-span-2 flex-1 bg-saas-blue rounded-3xl shadow-sm flex flex-col items-center justify-center relative overflow-hidden border-2 border-saas-ink/10 min-h-[500px]">
          <Sparkle className="absolute top-10 left-10 text-white w-16 h-16 opacity-50" />
          <ScribbleMark className="absolute bottom-10 right-10 text-saas-ink w-20 h-20 opacity-10" />

          {/* CSS Drawn Navy-Ink Character */}
          <div className="relative flex flex-col items-center">
            {/* Body */}
            <div className="w-48 h-40 border-[6px] border-saas-ink rounded-t-[80px] rounded-b-[40px] bg-white flex flex-col items-center justify-center relative shadow-xl z-10">
              {/* Face */}
              <div className="flex gap-8 mb-4">
                {/* Eyes */}
                <div className="w-4 h-8 bg-saas-ink rounded-full animate-bounce" style={{ animationDuration: '2s' }}></div>
                <div className="w-4 h-8 bg-saas-ink rounded-full animate-bounce" style={{ animationDuration: '2s', animationDelay: '0.1s' }}></div>
              </div>
              {/* Smile */}
              <svg width="40" height="20" viewBox="0 0 40 20" fill="none" stroke="#0F1B2D" strokeWidth="6" strokeLinecap="round">
                <path d="M 5 5 Q 20 20 35 5" />
              </svg>
            </div>
            {/* Neck / Shoulders */}
            <div className="w-64 h-24 border-[6px] border-saas-ink rounded-t-[60px] bg-white mt-[-20px] shadow-lg relative z-0"></div>
          </div>

          {/* Name Tag */}
          <div className="absolute bottom-6 left-6 bg-white/90 backdrop-blur px-5 py-2 rounded-xl border-2 border-saas-ink shadow-sm">
            <span className="font-bold text-sm">Alex (Your Coach)</span>
          </div>

        </div>

        {/* Small self-view tile */}
        <div className="absolute top-6 right-6 lg:right-auto lg:left-6 w-32 h-44 bg-saas-peach rounded-2xl border-2 border-saas-ink/10 shadow-lg overflow-hidden flex items-center justify-center z-20">
          <div className="text-saas-ink/40 font-bold text-center p-3 text-xs">Camera Off</div>
        </div>

        {/* Chat Panel */}
        <div className="lg:col-span-1 bg-gray-50 rounded-3xl shadow-sm border-2 border-saas-ink/10 flex flex-col overflow-hidden relative h-full">
          <div className="bg-white border-b-2 border-saas-ink/10 px-4 py-3 flex items-center justify-between z-10 shadow-sm">
            <span className="font-bold text-saas-ink">Live Transcript</span>
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          </div>

          <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-3 pb-6">
            {messages.length === 0 && (
              <div className="text-center text-gray-400 text-sm font-medium mt-10">Start speaking to see transcript...</div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={`max-w-[85%] rounded-2xl px-4 py-2 text-sm font-medium ${msg.type === "user_final"
                  ? "bg-saas-peach text-saas-ink self-end rounded-tr-sm border border-saas-ink/10 shadow-sm"
                  : "bg-white text-saas-ink self-start rounded-tl-sm border border-saas-ink/10 shadow-sm"
                }`}>
                <div className="text-[10px] opacity-50 mb-1">{msg.type === "user_final" ? "You" : "Alex"}</div>
                {msg.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>

      </div>

      {/* Bottom Controls */}
      <div className="w-full flex justify-center items-center gap-4 py-6 mt-2">

        <button className="w-12 h-12 flex items-center justify-center rounded-xl bg-white border-2 border-saas-ink/20 hover:border-saas-ink text-saas-ink transition-all shadow-sm hover:shadow-md">
          <Settings size={20} />
        </button>

        <button className="w-12 h-12 flex items-center justify-center rounded-xl bg-white border-2 border-saas-ink/20 hover:border-saas-ink text-saas-ink transition-all shadow-sm hover:shadow-md">
          <Volume2 size={20} />
        </button>

        <button className="px-8 py-4 rounded-xl bg-white border-2 border-saas-ink text-saas-ink hover:bg-saas-ink hover:text-white transition-all shadow-[0_4px_12px_rgba(15,27,45,0.1)] flex items-center gap-2 font-bold text-base">
          <Mic size={20} />
          Mute
        </button>

        <button
          onClick={() => navigate('/')}
          className="px-8 py-4 rounded-xl bg-red-500 hover:bg-red-600 text-white transition-all shadow-[0_4px_12px_rgba(239,68,68,0.3)] flex items-center gap-2 font-bold text-base border-2 border-red-600"
        >
          <PhoneOff size={20} />
          End Call
        </button>

      </div>
    </div>
  );
}
