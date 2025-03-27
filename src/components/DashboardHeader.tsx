
import React from 'react';
import { Filter, RefreshCw } from 'lucide-react';

interface DashboardHeaderProps {
  title: string;
  subtitle?: string;
  onRefresh?: () => void;
  onFilterToggle?: () => void;
}

const DashboardHeader: React.FC<DashboardHeaderProps> = ({
  title,
  subtitle,
  onRefresh,
  onFilterToggle
}) => {
  return (
    <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">{title}</h1>
        {subtitle && <p className="mt-1 text-sm text-gray-600">{subtitle}</p>}
      </div>
      <div className="flex items-center space-x-2 mt-3 md:mt-0">
        <button 
          onClick={onFilterToggle}
          className="px-3 py-2 border border-gray-200 rounded-md bg-white text-gray-700 text-sm flex items-center space-x-1 transition-all hover:border-gray-300 hover:bg-gray-50"
        >
          <Filter size={16} />
          <span>Filter</span>
        </button>
        <button 
          onClick={onRefresh}
          className="px-3 py-2 border border-gray-200 rounded-md bg-white text-gray-700 text-sm flex items-center space-x-1 transition-all hover:border-gray-300 hover:bg-gray-50"
        >
          <RefreshCw size={16} />
          <span>Refresh</span>
        </button>
      </div>
    </div>
  );
};

export default DashboardHeader;
