// src/App.jsx
import React, { useState, useEffect } from 'react';
import ActivationList from './components/ActivationList';
import './index.css';

export default function App() {
  const [activations, setActivations] = useState([]);
  const callsign = 'EA3GNU'; // dinámico según sesión/bot

  useEffect(() => {
    // Ejemplo: cargar JSON local o fetch a tu backend
    import('./demo-activations.json').then(m => setActivations(m.default));
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>{callsign}</h1>
        <p>Total SOTA points: {/* aquí sumas puntos */}</p>
      </header>
      <main>
        <ActivationList activations={activations} />
      </main>
    </div>
  );
}
