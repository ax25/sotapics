import ActivationCard from './components/ActivationCard';

function App() {
  return (
    <div className="min-h-screen bg-slate-50 p-4">
      <h1 className="text-2xl font-bold mb-4">EA3GNU – Activaciones SOTA</h1>

      {/* Tarjeta de ejemplo. Sustituye las props por datos reales más adelante */}
      <ActivationCard
        date="2025‑06‑26"
        refCode="EA3/GI-014"
        summitName="Taga"
        altitude={2039}
        points={8}
        qsoCount={57}
        photoUrls={[
          '/photos/EA3GNU/EA3-GI-014_2025-06-26/photo_1.jpg',
          '/photos/EA3GNU/EA3-GI-014_2025-06-26/photo_2.jpg',
          '/photos/EA3GNU/EA3-GI-014_2025-06-26/photo_3.jpg',
        ]}
        dxcc="EA"
      />
    </div>
  );
}

export default App;
