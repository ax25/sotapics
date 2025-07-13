// src/components/ActivationCard.jsx
import React from 'react';
import styles from './ActivationCard.module.css';

export default function ActivationCard({ activation }) {
  const { summitName, elevation, ref, date, qsos, photos } = activation;

  return (
    <div className={styles.card}>
      {/* Franja superior semi-transparente */}
      <div className={styles.topStripe}>
        <h2>
          🗻 {summitName} <span className={styles.elevation}>({elevation} m)</span>
        </h2>
      </div>

      {/* Foto principal */}
      <div className={styles.photoContainer}>
        <img src={photos[0]} alt={summitName} className={styles.photo} />
      </div>

      {/* Franja inferior con datos */}
      <div className={styles.bottomStripe}>
        <div className={styles.leftInfo}>
          🆔 <strong>Ref:</strong> {ref} • ⛰️ {elevation} m • ⭐ {activation.points}
        </div>
        <div className={styles.rightInfo}>
          📅 {date} • 📶 {qsos} QSOs
        </div>
      </div>
    </div>
  );
}
