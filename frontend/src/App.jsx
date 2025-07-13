import React, { useEffect, useState } from "react";
import ActivationsList from "./ActivationsList";
import "./App.css";

export default function App() {
  const [activations, setActivations] = useState([]);

  useEffect(() => {
    fetch("/src/demo-activations.json")
      .then((res) => res.json())
      .then(setActivations)
      .catch(console.error);
  }, []);

  return (
    <main className="container">
      <h1 className="text-3xl font-bold mb-6">EA3GNU Activations</h1>
      {activations.length > 0 ? (
        <ActivationsList activations={activations} />
      ) : (
        <p>Loading...</p>
      )}
    </main>
  );
}
