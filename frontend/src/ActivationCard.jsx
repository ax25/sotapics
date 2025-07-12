import React from 'react';
import './ActivationCard.css';

export default function ActivationCard({ activation }) {
  const { date, ref, name, elevation, points, photos } = activation;
  const formattedDate = new Date(date).toLocaleDateString();

  return (
    <div className="activation-card">
      <header>
        <h3>{ref}</h3>
        <span className="date">{formattedDate}</span>
      </header>

      <p className="subtitle">
        {name} &bull; {elevation} m &bull; {points} pts
      </p>

      <div className="photos">
        {photos.map((url, i) => (
          <img key={i} src={url} alt={`${ref} photo ${i + 1}`} />
        ))}
      </div>
    </div>
  );
}
