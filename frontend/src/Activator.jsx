// frontend/src/Activator.jsx
import { useEffect, useState } from "react";

export default function Activator({ callsign }) {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const ws = new WebSocket(`ws://${location.host}/ws/${callsign}`);
    ws.onmessage = e => setItems(prev => [JSON.parse(e.data), ...prev]);
    return () => ws.close();
  }, [callsign]);

  return (
    <div className="flex flex-wrap gap-4 p-4">
      {items.map(p => (
        <div key={p.url} className="w-64 shadow rounded overflow-hidden">
          <img src={p.url} className="h-40 w-full object-cover" />
          <div className="p-2 text-sm">
            <strong>{p.ref}</strong><br/>
            {new Date(p.ts).toLocaleDateString()}
          </div>
        </div>
      ))}
    </div>
  );
}
