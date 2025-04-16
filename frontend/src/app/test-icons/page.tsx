'use client';

import { FiFileText, FiGlobe, FiClock, FiUsers } from 'react-icons/fi';

export default function TestIcons() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Testing React Icons</h1>
      <div className="flex space-x-4">
        <div className="flex flex-col items-center">
          <FiFileText size={24} />
          <span>FiFileText</span>
        </div>
        <div className="flex flex-col items-center">
          <FiGlobe size={24} />
          <span>FiGlobe</span>
        </div>
        <div className="flex flex-col items-center">
          <FiClock size={24} />
          <span>FiClock</span>
        </div>
        <div className="flex flex-col items-center">
          <FiUsers size={24} />
          <span>FiUsers</span>
        </div>
      </div>
    </div>
  );
}
