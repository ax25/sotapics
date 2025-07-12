import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/components/ui/card";
import { ChevronLeft, ChevronRight, MapPin, Radio } from "lucide-react";

interface ActivationCardProps {
  date: string; // ISO string
  sotaRef: string;
  summitName: string;
  altitude: number; // metres
  points: number;
  qsos: number;
  photos: string[]; // absolute or relative URLs (served from /uploads)
  flagUrl?: string; // optional URL to PNG/SVG flag
}

const ActivationCard: React.FC<ActivationCardProps> = ({
  date,
  sotaRef,
  summitName,
  altitude,
  points,
  qsos,
  photos,
  flagUrl,
}) => {
  const [idx, setIdx] = useState(0);
  const next = () => setIdx((idx + 1) % photos.length);
  const prev = () => setIdx((idx - 1 + photos.length) % photos.length);

  const formattedDate = new Date(date).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  return (
    <Card className="relative w-full max-w-sm rounded-2xl shadow-lg overflow-hidden bg-white dark:bg-slate-900">
      <CardHeader className="flex flex-row items-center gap-2 p-4 border-b">
        {flagUrl && (
          <img
            src={flagUrl}
            alt="flag"
            className="w-6 h-4 rounded-sm object-cover border"
          />
        )}
        <CardTitle className="text-base font-semibold flex-1 truncate">
          {sotaRef}
        </CardTitle>
        <span className="text-sm text-slate-500 dark:text-slate-400">
          {formattedDate}
        </span>
      </CardHeader>

      {/* Photo carousel */}
      {photos.length > 0 && (
        <div className="relative group">
          <AnimatePresence mode="wait" initial={false}>
            <motion.img
              key={photos[idx]}
              src={photos[idx]}
              alt={`Activation photo ${idx + 1}`}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="h-48 w-full object-cover"
            />
          </AnimatePresence>
          {/* Navigation buttons (visible on hover) */}
          {photos.length > 1 && (
            <>
              <button
                onClick={prev}
                className="absolute left-2 top-1/2 -translate-y-1/2 bg-black/40 p-1 rounded-full text-white opacity-0 group-hover:opacity-100 transition"
              >
                <ChevronLeft size={20} />
              </button>
              <button
                onClick={next}
                className="absolute right-2 top-1/2 -translate-y-1/2 bg-black/40 p-1 rounded-full text-white opacity-0 group-hover:opacity-100 transition"
              >
                <ChevronRight size={20} />
              </button>
            </>
          )}
          {/* Dots */}
          {photos.length > 1 && (
            <div className="absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-1">
              {photos.map((_, i) => (
                <span
                  key={i}
                  className={`h-2 w-2 rounded-full ${
                    i === idx ? "bg-white" : "bg-white/40"
                  }`}
                />
              ))}
            </div>
          )}
        </div>
      )}

      <CardContent className="p-4 grid grid-cols-2 gap-2 text-sm">
        <div className="flex items-center gap-1">
          <MapPin size={16} className="text-teal-600 dark:text-teal-400" />
          <span className="truncate" title={summitName}>
            {summitName}
          </span>
        </div>
        <div className="text-right text-slate-500 dark:text-slate-400">
          {altitude} m
        </div>
        <div className="flex items-center gap-1">
          <span className="font-medium">{points}</span>
          <span className="text-slate-500 dark:text-slate-400">pts</span>
        </div>
        <div className="flex items-center justify-end gap-1">
          <Radio size={16} className="text-indigo-600 dark:text-indigo-400" />
          <span>{qsos}</span>
        </div>
      </CardContent>
    </Card>
  );
};

export default ActivationCard;
