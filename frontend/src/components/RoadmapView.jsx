import React, { useState } from 'react';
import ReasoningTrace from './ReasoningTrace';

const LEVEL_COLOR = {
  beginner: 'bg-green-900 text-green-300 border-green-700',
  intermediate: 'bg-yellow-900 text-yellow-300 border-yellow-700',
  advanced: 'bg-red-900 text-red-300 border-red-700',
};

const PRIORITY_BADGE = {
  'must-have': 'bg-indigo-700 text-indigo-100',
  'nice-to-have': 'bg-gray-700 text-gray-300',
  'prerequisite': 'bg-purple-900 text-purple-300',
};

function SkillCard({ module, index }) {
  const [expanded, setExpanded] = useState(false);
  const levelClass = LEVEL_COLOR[module.target_level] || LEVEL_COLOR.beginner;
  const priorityClass = PRIORITY_BADGE[module.priority] || PRIORITY_BADGE['nice-to-have'];

  return (
    <div className="relative flex gap-4">
      {/* Timeline connector */}
      <div className="flex flex-col items-center">
        <div className="w-9 h-9 rounded-full bg-indigo-600 flex items-center justify-center font-bold text-sm shrink-0 z-10">
          {index + 1}
        </div>
        <div className="w-0.5 bg-gray-700 flex-1 mt-1" />
      </div>

      {/* Card */}
      <div className="flex-1 mb-6 bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
        <div
          className="flex items-center justify-between px-5 py-4 cursor-pointer hover:bg-gray-700 transition-colors"
          onClick={() => setExpanded(!expanded)}>
          <div className="flex items-center gap-3 flex-wrap">
            <span className="font-semibold capitalize text-white">{module.skill}</span>
            <span className={`text-xs px-2 py-0.5 rounded-full border ${levelClass}`}>
              → {module.target_level}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full ${priorityClass}`}>
              {module.priority}
            </span>
            {module.is_prerequisite && (
              <span className="text-xs px-2 py-0.5 rounded-full bg-purple-900 text-purple-300">prereq</span>
            )}
          </div>
          <div className="flex items-center gap-3 shrink-0">
            <span className="text-xs text-gray-400">{module.estimated_hours}h</span>
            <span className="text-gray-500 text-sm">{expanded ? '▲' : '▼'}</span>
          </div>
        </div>

        {expanded && (
          <div className="border-t border-gray-700 px-5 py-4 space-y-3">
            <p className="text-xs text-gray-400">
              Current: <span className="text-white">{module.current_level || 'none'}</span>
              {' → '}
              Target: <span className="text-white">{module.target_level}</span>
            </p>
            <div className="space-y-2">
              {module.courses.length === 0 ? (
                <p className="text-sm text-gray-500 italic">No catalog courses found — search online resources.</p>
              ) : (
                module.courses.map((course, ci) => (
                  <a key={ci} href={course.url} target="_blank" rel="noreferrer"
                    className="flex items-center justify-between p-3 bg-gray-900 rounded-lg hover:bg-gray-700 transition-colors group">
                    <div>
                      <p className="text-sm font-medium text-indigo-300 group-hover:text-indigo-200">{course.title}</p>
                      <p className="text-xs text-gray-500 capitalize">{course.level} · {course.duration}</p>
                    </div>
                    <span className="text-gray-600 group-hover:text-gray-400 text-xs">↗</span>
                  </a>
                ))
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function RoadmapView({ data }) {
  const { pathway } = data;

  return (
    <div className="w-full max-w-3xl mx-auto space-y-8">
      {/* Summary */}
      <div className="bg-gray-800 rounded-2xl p-6 border border-gray-700">
        <h2 className="text-xl font-bold text-white mb-1">
          {pathway.current_role || 'Current Role'} → {pathway.target_role || 'Target Role'}
        </h2>
        <p className="text-gray-400 text-sm mb-4">
          Domain: <span className="capitalize text-indigo-300">{pathway.domain}</span>
        </p>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div className="bg-gray-900 rounded-xl p-3">
            <p className="text-2xl font-bold text-indigo-400">{pathway.total_modules}</p>
            <p className="text-xs text-gray-500 mt-1">Learning Modules</p>
          </div>
          <div className="bg-gray-900 rounded-xl p-3">
            <p className="text-2xl font-bold text-green-400">{pathway.skills_already_proficient.length}</p>
            <p className="text-xs text-gray-500 mt-1">Skills You Have</p>
          </div>
          <div className="bg-gray-900 rounded-xl p-3">
            <p className="text-2xl font-bold text-yellow-400">{pathway.total_estimated_hours}h</p>
            <p className="text-xs text-gray-500 mt-1">Est. Learning Time</p>
          </div>
        </div>
      </div>

      {/* Already proficient */}
      {pathway.skills_already_proficient.length > 0 && (
        <div className="bg-gray-800 rounded-xl p-5 border border-green-800">
          <p className="text-sm font-semibold text-green-400 mb-3">Already Proficient — Skip These</p>
          <div className="flex flex-wrap gap-2">
            {pathway.skills_already_proficient.map((s, i) => (
              <span key={i} className="text-xs bg-green-900 text-green-300 border border-green-700 px-3 py-1 rounded-full capitalize">
                {s}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Pathway */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-4">Your Personalized Learning Pathway</h3>
        {pathway.modules.map((module, i) => (
          <SkillCard key={i} module={module} index={i} />
        ))}
      </div>

      {/* Reasoning trace */}
      <ReasoningTrace steps={pathway.reasoning_trace} />
    </div>
  );
}
