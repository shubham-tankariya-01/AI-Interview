import { useNavigate } from 'react-router-dom';
import { Sparkle, SquiggleUnderline, CurvedArrow, ScribbleMark } from '../components/Doodles';

const AVATARS = [
  "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80"
];

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="flex-1 flex flex-col items-center">
      
      {/* Hero Section */}
      <section className="w-full max-w-5xl mx-auto px-6 pt-16 pb-24 text-center relative">
        <Sparkle className="absolute top-12 left-16 text-saas-amber w-10 h-10" />
        <ScribbleMark className="absolute bottom-16 right-16 text-saas-blue w-12 h-12" />

        <div className="inline-block bg-saas-peach px-5 py-2 rounded-xl mb-6 shadow-sm">
          <span className="font-bold text-xs text-saas-ink">✨ New: System Design Scenarios</span>
        </div>

        <h1 className="text-5xl md:text-7xl font-brand font-extrabold text-saas-ink leading-[1.1] tracking-tight mb-6 relative z-10">
          Nail your next interview with <span className="relative inline-block">confidence.<SquiggleUnderline className="absolute -bottom-2 left-0 text-saas-amber" /></span>
        </h1>
        
        <p className="text-lg text-saas-ink/70 font-medium max-w-2xl mx-auto mb-10 leading-relaxed">
          Practice with a friendly AI coach. Get real-time feedback, overcome your nerves, and land your dream job without breaking a sweat.
        </p>

        <button
          onClick={() => navigate('/setup')}
          className="bg-saas-amber hover:bg-orange-500 text-saas-ink font-bold text-lg py-4 px-8 rounded-xl shadow-[0_8px_20px_rgba(242,169,59,0.3)] transition-all transform hover:-translate-y-1 inline-flex items-center gap-2"
        >
          Start Practice Session
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
        </button>

        {/* Circular Avatar Cluster */}
        <div className="mt-20 flex flex-col items-center relative">
          <CurvedArrow className="absolute -left-12 -top-8 text-saas-ink/40 w-16 h-16 transform -rotate-12" />
          <p className="text-sm font-bold text-saas-ink/60 mb-6 uppercase tracking-widest">Join 10,000+ candidates who got hired</p>
          <div className="flex items-center -space-x-4">
            {AVATARS.map((url, i) => (
              <div key={i} className={`relative p-1 rounded-full ${
                i === 0 ? 'bg-pink-200' : i === 1 ? 'bg-saas-blue' : i === 2 ? 'bg-saas-yellow' : 'bg-green-200'
              }`}>
                <img src={url} alt={`Avatar ${i+1}`} className="w-16 h-16 rounded-full border-4 border-white object-cover" />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature / Testimonial Section */}
      <section className="w-full bg-saas-yellow px-6 py-16 border-t-2 border-saas-ink/5">
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-3xl md:text-5xl font-brand font-extrabold text-saas-ink mb-5">
              Feedback that actually helps.
            </h2>
            <p className="text-lg text-saas-ink/80 mb-6">
              No robotic grading. The AI coach highlights your strengths and helps you refine your answers using natural, conversational feedback.
            </p>
            <div className="flex gap-3">
              <div className="bg-white px-4 py-2 rounded-xl font-semibold text-xs shadow-sm flex items-center gap-2">
                <span className="w-2 h-2 bg-green-400 rounded-full"></span> Behavioral
              </div>
              <div className="bg-white px-4 py-2 rounded-xl font-semibold text-xs shadow-sm flex items-center gap-2">
                <span className="w-2 h-2 bg-blue-400 rounded-full"></span> Technical
              </div>
            </div>
          </div>

          <div className="relative">
            <div className="absolute inset-0 bg-saas-peach transform rotate-3 rounded-3xl shadow-lg"></div>
            <div className="relative bg-white rounded-3xl p-8 shadow-xl z-10 border border-saas-ink/10">
              <Sparkle className="absolute -top-5 -right-5 text-saas-amber w-12 h-12" />
              <div className="flex items-center gap-3 mb-5">
                <img src={AVATARS[0]} className="w-10 h-10 rounded-full object-cover" alt="User" />
                <div>
                  <h4 className="font-bold text-sm">Sarah Jenkins</h4>
                  <p className="text-xs text-saas-ink/60">Product Designer</p>
                </div>
              </div>
              <p className="text-lg font-medium leading-relaxed">
                "I was terrified of behavioral rounds. Practicing with the AI felt like talking to a real mentor. I walked into my final round completely relaxed and got the offer!"
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Oversized Footer */}
      <footer className="w-full bg-saas-ink text-white pt-16 pb-8 px-6 flex flex-col items-center text-center overflow-hidden">
        <h2 className="text-[10vw] font-brand font-extrabold leading-none tracking-tighter mb-8 text-saas-amber">
          Coach.ai
        </h2>
        <div className="flex gap-6 text-white/60 font-medium text-base">
          <a href="#" className="hover:text-white">Twitter</a>
          <a href="#" className="hover:text-white">LinkedIn</a>
          <a href="#" className="hover:text-white">Privacy</a>
          <a href="#" className="hover:text-white">Terms</a>
        </div>
      </footer>
    </div>
  );
}
