import React, { useState } from 'react';

export default function ReasoningTrace({ steps }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="mt-6 border border-gray-700 rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex justify-between items-center px-5 py-4 bg-gray-800 hover:bg-gray-700 text-left transition-colors">
        <span className="font-semibold text-indigo-300">Reasoning Trace</span>
        <span className="text-gray-400 text-sm">{open ? '▲ Hide' : '▼ Show'}</span>
      </button>
      {open && (
        <div className="bg-gray-900 px-5 py-4 space-y-2">
          {steps.map((step, i) => (
            <div key={i} className="flex gap-3 text-sm">
              <span className="text-indigo-500 font-mono shrink-0">{String(i + 1).padStart(2, '0')}</span>
              <span className="text-gray-300">{step}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
