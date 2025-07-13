// src/components/ActivationList.jsx
import React from 'react';
import ActivationCard from './ActivationCard';

export default function ActivationList({ activations }) {
  return (
    <div>
      {activations.map(act => (
        <ActivationCard key={act.ref + act.date} activation={act} />
      ))}
    </div>
  );
}
