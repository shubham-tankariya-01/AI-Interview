import { useNavigate } from 'react-router-dom';
import { Mic, PhoneOff, Settings, Volume2 } from 'lucide-react';
import { ScribbleMark, Sparkle } from '../components/Doodles';

export default function Interview() {
  const navigate = useNavigate();

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

      {/* Main Video Area */}
      <div className="flex-1 w-full max-w-5xl mx-auto flex flex-col relative">
        
        {/* Main Caller Tile (The Coach) */}
        <div className="flex-1 bg-saas-blue rounded-3xl shadow-sm flex flex-col items-center justify-center relative overflow-hidden border-2 border-saas-ink/10">
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
        <div className="absolute top-6 right-6 w-40 h-56 bg-saas-peach rounded-2xl border-2 border-saas-ink/10 shadow-lg overflow-hidden flex items-center justify-center">
          <div className="text-saas-ink/40 font-bold text-center p-3 text-sm">Camera Off</div>
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
