import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkle, SquiggleUnderline } from '../components/Doodles';
import { Smile, Brain, Zap } from 'lucide-react';

export default function Setup() {
  const navigate = useNavigate();
  const [difficulty, setDifficulty] = useState('Medium');

  const options = [
    {
      level: 'Easy',
      desc: 'Friendly, gentle feedback. Great for warming up.',
      icon: Smile,
      color: 'bg-saas-peach'
    },
    {
      level: 'Medium',
      desc: 'Standard interview pacing and constructive critique.',
      icon: Brain,
      color: 'bg-saas-yellow'
    },
    {
      level: 'Hard',
      desc: 'Fast-paced, high pressure. For the ultimate test.',
      icon: Zap,
      color: 'bg-saas-blue'
    }
  ];

  return (
    <div className="max-w-4xl mx-auto w-full pt-12 pb-16 px-6">
      
      <div className="text-center mb-12 relative">
        <Sparkle className="absolute -top-6 -left-6 text-saas-amber w-12 h-12 hidden md:block" />
        <h2 className="text-4xl md:text-6xl font-brand font-extrabold text-saas-ink tracking-tight mb-3 relative z-10">
          Set the stage.
        </h2>
        <p className="text-xl text-saas-ink/70 max-w-2xl mx-auto">
          Choose how intense you want this session to be. You can always change it later.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-16 relative">
        {/* Decorative background blob */}
        <div className="absolute inset-0 bg-saas-peach rounded-[80px] blur-3xl opacity-50 -z-10 transform scale-110"></div>
        
        {options.map((opt, i) => {
          const Icon = opt.icon;
          const isSelected = difficulty === opt.level;
          // Apply slight tilt depending on index
          const tilt = i === 0 ? '-rotate-2' : i === 1 ? 'rotate-2' : '-rotate-1';
          
          return (
            <button
              key={opt.level}
              onClick={() => setDifficulty(opt.level)}
              className={`text-left relative transition-all duration-300 ease-in-out group ${
                isSelected ? 'transform scale-105 z-10' : `hover:scale-105 ${tilt}`
              }`}
            >
              <div className={`absolute inset-0 rounded-2xl shadow-xl transition-opacity ${
                isSelected ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'
              } ${opt.color}`}></div>
              
              <div className={`relative h-full bg-white rounded-2xl p-6 border-4 transition-colors ${
                isSelected ? 'border-saas-ink' : 'border-transparent shadow-lg'
              }`}>
                <div className={`w-12 h-12 rounded-full flex items-center justify-center mb-5 ${opt.color}`}>
                  <Icon size={24} className="text-saas-ink" />
                </div>
                <h3 className="text-2xl font-brand font-bold text-saas-ink mb-2">{opt.level}</h3>
                <p className="text-base text-saas-ink/70 leading-relaxed font-medium">
                  {opt.desc}
                </p>
              </div>
            </button>
          );
        })}
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-10 border-t-2 border-saas-ink/10">
        <button
          onClick={() => navigate('/')}
          className="px-6 py-3 font-bold text-lg text-saas-ink/60 hover:text-saas-ink bg-transparent border-2 border-transparent hover:bg-saas-ink/5 rounded-xl transition-all"
        >
          Nevermind
        </button>
        <button
          onClick={() => navigate('/interview')}
          className="px-8 py-3 font-bold text-lg bg-saas-amber text-saas-ink hover:bg-orange-500 rounded-xl shadow-lg hover:-translate-y-1 transition-all"
        >
          Connect to Coach
        </button>
      </div>
      
    </div>
  );
}
