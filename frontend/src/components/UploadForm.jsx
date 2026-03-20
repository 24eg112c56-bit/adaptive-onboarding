import React, { useState } from 'react';
import axios from 'axios';

export default function UploadForm({ onResult, onLoading }) {
  const [resume, setResume] = useState(null);
  const [jd, setJd] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resume || !jd) {
      setError('Please upload both files.');
      return;
    }
    setError('');
    onLoading(true);
    const form = new FormData();
    form.append('resume', resume);
    form.append('job_description', jd);
    try {
      const res = await axios.post('http://localhost:8001/analyze', form);
      onResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong. Check your API key and try again.');
    } finally {
      onLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-6 w-full max-w-xl mx-auto">
      <div className="flex flex-col gap-2">
        <label className="text-sm text-gray-400 font-medium">Resume (PDF or TXT)</label>
        <div
          className="border-2 border-dashed border-gray-700 rounded-xl p-6 text-center hover:border-indigo-500 transition-colors cursor-pointer"
          onClick={() => document.getElementById('resume-input').click()}>
          <input id="resume-input" type="file" accept=".pdf,.txt" className="hidden"
            onChange={e => setResume(e.target.files[0])} />
          {resume
            ? <p className="text-indigo-400 font-medium">{resume.name}</p>
            : <p className="text-gray-500">Click to upload resume</p>}
        </div>
      </div>

      <div className="flex flex-col gap-2">
        <label className="text-sm text-gray-400 font-medium">Job Description (PDF or TXT)</label>
        <div
          className="border-2 border-dashed border-gray-700 rounded-xl p-6 text-center hover:border-indigo-500 transition-colors cursor-pointer"
          onClick={() => document.getElementById('jd-input').click()}>
          <input id="jd-input" type="file" accept=".pdf,.txt" className="hidden"
            onChange={e => setJd(e.target.files[0])} />
          {jd
            ? <p className="text-indigo-400 font-medium">{jd.name}</p>
            : <p className="text-gray-500">Click to upload job description</p>}
        </div>
      </div>

      {error && <p className="text-red-400 text-sm text-center">{error}</p>}

      <button type="submit"
        className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 rounded-xl transition-colors">
        Generate My Learning Pathway
      </button>
    </form>
  );
}
