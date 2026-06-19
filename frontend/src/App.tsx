/**
 * Main App Component
 */
import React, { useEffect } from 'react';
import { HomePage } from './presentation/pages/Home';
import { initializeDIContainer } from './application/diContainer';
import './App.css';

function App() {
  useEffect(() => {
    // Initialize DI container with API base URL from environment
    const apiBaseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api/v1';
    initializeDIContainer(apiBaseURL);
  }, []);

  return (
    <div className="app">
      <HomePage />
    </div>
  );
}

export default App;
