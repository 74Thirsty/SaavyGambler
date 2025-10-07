import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import './App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard/:sport" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
