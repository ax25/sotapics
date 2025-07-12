import React, { useEffect, useState } from 'react';
import ActivationCard from './ActivationCard';

/**
 * Loads activations from `/data/activations.json`.
 * Replace this with a call to your real backend later.
 */
export default function ActivationsList() {
  const [activations, setActivations] = useState([]);

  useEffect(() => {
    fetch('/data/activations.json')
      .then((r) => r.json())
      .then(setActivations)
      .catch(console.error);
  }, []);

  if (!activations.length) return <p>Loading activations…</p>;

  return (
    <section>
      {activations.map((a) => (
        <ActivationCard key={`${a.ref}-${a.date}`} activation={a} />
      ))}
    </section>
  );
}
