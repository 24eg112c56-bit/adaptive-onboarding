import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import RoadmapView from './components/RoadmapView';

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const reset = () => setResult(null);

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-sm font-bold">AI</div>
          <span className="font-semibold text-white">AI-Adaptive Onboarding Engine</span>
        </div>
        {result && (
          <button onClick={reset} className="text-sm text-gray-400 hover:text-white transition-colors">
            ← Start Over
          </button>
        )}
      </header>

      <main className="px-6 py-12">
        {!result && !loading && (
          <div className="text-center mb-10">
            <h1 className="text-4xl font-bold text-white mb-3">
              AI-Adaptive <span className="text-indigo-400">Onboarding Engine</span>
            </h1>
            <p className="text-gray-400 max-w-lg mx-auto">
              Upload your resume and a job description. Our AI will identify your skill gaps
              and generate an optimized, step-by-step training pathway.
            </p>
          </div>
        )}

        {loading && (
          <div className="flex flex-col items-center justify-center py-24 gap-4">
            <div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin" />
            <p className="text-gray-400">Analyzing your profile and generating pathway...</p>
          </div>
        )}

        {!loading && !result && <UploadForm onResult={setResult} onLoading={setLoading} />}
        {!loading && result && <RoadmapView data={result} />}
      </main>
    </div>
  );
}
