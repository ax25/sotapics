import React from 'react';
import ActivationsList from './ActivationsList';

export default function App() {
  return (
    <main style={{ maxWidth: 900, margin: '0 auto', padding: '1rem' }}>
      <h1>SOTApics – latest activations</h1>
      <ActivationsList />
    </main>
  );
}
