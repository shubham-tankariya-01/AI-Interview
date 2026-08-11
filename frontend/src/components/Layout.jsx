import { Outlet, Link, useLocation } from 'react-router-dom';

export default function Layout() {
  const location = useLocation();
  
  return (
    <div className="min-h-screen flex bg-white text-saas-ink font-body">
      
      {/* Sidebar - Pastel Background */}
      <aside className="w-64 bg-saas-peach p-6 hidden md:flex flex-col border-r-2 border-saas-ink/5">
        
        <div className="mb-10">
          <h1 className="text-2xl font-brand font-extrabold text-saas-ink tracking-tight flex items-center gap-2">
            Coach<span className="text-saas-amber">.ai</span>
          </h1>
        </div>

        <nav className="flex-1 space-y-3">
          <Link 
            to="/" 
            className={`block px-4 py-3 font-semibold text-base transition-all rounded-xl ${
              location.pathname === '/' || location.pathname === '/setup'
                ? 'bg-saas-ink text-white' 
                : 'text-saas-ink hover:bg-white/50'
            }`}
          >
            Dashboard
          </Link>
          <div className="block px-4 py-3 font-medium text-base text-saas-ink/40 cursor-not-allowed">
            Interviews
          </div>
          <div className="block px-4 py-3 font-medium text-base text-saas-ink/40 cursor-not-allowed">
            Feedback
          </div>
          <div className="block px-4 py-3 font-medium text-base text-saas-ink/40 cursor-not-allowed">
            Settings
          </div>
        </nav>

        <div className="mt-auto bg-white/60 p-5 rounded-2xl">
          <p className="text-sm font-semibold mb-2">Need help?</p>
          <p className="text-xs text-saas-ink/70 mb-4">Check out our guide to acing your next interview.</p>
          <button className="text-xs font-bold bg-white px-4 py-2 rounded-lg transition-colors w-full hover:bg-gray-50">
            Read Guide
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-screen overflow-y-auto">
        
        {/* Mobile Header */}
        <header className="md:hidden flex items-center justify-between p-6 bg-saas-peach border-b border-saas-ink/10">
          <h1 className="text-2xl font-brand font-extrabold text-saas-ink tracking-tight">
            Coach<span className="text-saas-amber">.ai</span>
          </h1>
          <button className="bg-saas-ink text-white px-4 py-2 rounded-full font-semibold text-sm">
            Menu
          </button>
        </header>

        <div className="flex-1 flex flex-col">
          <Outlet />
        </div>
      </main>
      
    </div>
  );
}
