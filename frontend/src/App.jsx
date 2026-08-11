// Eventual Purpose: Root application component holding global state providers and router configuration.
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Setup from './pages/Setup';
import Interview from './pages/Interview';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="setup" element={<Setup />} />
        </Route>
        <Route path="/interview" element={<Interview />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
