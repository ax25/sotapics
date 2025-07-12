import { useState } from 'react';

interface Props {
  date: string;
  refCode: string;
  summitName: string;
  altitude: number;
  points: number;
  qsoCount: number;
  photoUrls: string[];
  dxcc: string; // Código DXCC para mostrar la bandera
}

function getFlagEmoji(code: string) {
  return code
    .toUpperCase()
    .replace(/./g, (char) =>
      String.fromCodePoint(127397 + char.charCodeAt(0)),
    );
}

export default function ActivationCard({
  date,
  refCode,
  summitName,
  altitude,
  points,
  qsoCount,
  photoUrls,
  dxcc,
}: Props) {
  const [index, setIndex] = useState(0);

  const prev = () =>
    setIndex((index - 1 + photoUrls.length) % photoUrls.length);
  const next = () => setIndex((index + 1) % photoUrls.length);

  return (
    <div className="bg-white rounded-2xl shadow p-4 mb-6 max-w-md">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-gray-500">{date}</span>
        <span className="text-lg font-semibold">
          {getFlagEmoji(dxcc)} {refCode}
        </span>
      </div>

      <h2 className="text-xl font-bold mb-1">{summitName}</h2>
      <p className="text-sm text-gray-600 mb-4">
        {altitude} m · {points} pts · {qsoCount} QSOs
      </p>

      <div className="relative">
        <img
          src={photoUrls[index]}
          alt={\`Foto \${index + 1}\`}
          className="w-full h-48 object-cover rounded-xl"
        />
        {photoUrls.length > 1 && (
          <>
            <button
              onClick={prev}
              className="absolute left-1 top-1/2 -translate-y-1/2 bg-white/80 rounded-full p-1 select-none"
            >
              ‹
            </button>
            <button
              onClick={next}
              className="absolute right-1 top-1/2 -translate-y-1/2 bg-white/80 rounded-full p-1 select-none"
            >
              ›
            </button>
          </>
        )}
      </div>
    </div>
  );
}
