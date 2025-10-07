import { useParams, useNavigate } from 'react-router-dom';
import { useState } from 'react';

interface TabType {
  id: string;
  name: string;
  icon: string;
}

const tabs: TabType[] = [
  { id: 'stats', name: 'Statistics', icon: '📊' },
  { id: 'spread', name: 'Point Spread', icon: '📈' },
  { id: 'fantasy', name: 'Fantasy', icon: '🏆' },
  { id: 'predictions', name: 'Predictions', icon: '🎯' }
];

function Dashboard() {
  const { sport } = useParams<{ sport: string }>();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('stats');

  const sportName = sport?.toUpperCase() || 'SPORT';

  const renderTabContent = () => {
    switch (activeTab) {
      case 'stats':
        return (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
            <h3 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
              Statistics Dashboard
            </h3>
            <div className="space-y-4">
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <p className="text-sm text-gray-600 dark:text-gray-400">Team Statistics</p>
                <p className="text-gray-800 dark:text-white">
                  Real-time team performance data will be displayed here using public sports APIs
                </p>
              </div>
              <div className="border-l-4 border-green-500 pl-4 py-2">
                <p className="text-sm text-gray-600 dark:text-gray-400">Player Statistics</p>
                <p className="text-gray-800 dark:text-white">
                  Individual player stats, trends, and performance metrics
                </p>
              </div>
              <div className="border-l-4 border-purple-500 pl-4 py-2">
                <p className="text-sm text-gray-600 dark:text-gray-400">Season Overview</p>
                <p className="text-gray-800 dark:text-white">
                  Season standings, schedules, and historical data
                </p>
              </div>
            </div>
          </div>
        );
      case 'spread':
        return (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
            <h3 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
              Point Spread Analysis
            </h3>
            <div className="space-y-4">
              <div className="bg-gradient-to-r from-blue-50 to-blue-100 dark:from-gray-700 dark:to-gray-600 rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 dark:text-white mb-2">Upcoming Games</h4>
                <p className="text-gray-600 dark:text-gray-300">
                  Point spread predictions for upcoming matchups based on historical data and current form
                </p>
              </div>
              <div className="bg-gradient-to-r from-green-50 to-green-100 dark:from-gray-700 dark:to-gray-600 rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 dark:text-white mb-2">Line Movement</h4>
                <p className="text-gray-600 dark:text-gray-300">
                  Track betting line movements and identify value opportunities
                </p>
              </div>
            </div>
          </div>
        );
      case 'fantasy':
        return (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
            <h3 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
              Fantasy Sports Insights
            </h3>
            <div className="space-y-4">
              <div className="border border-yellow-500 rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 dark:text-white mb-2">🌟 Top Performers</h4>
                <p className="text-gray-600 dark:text-gray-300">
                  Players with the highest projected fantasy points this week
                </p>
              </div>
              <div className="border border-red-500 rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 dark:text-white mb-2">⚠️ Injury Reports</h4>
                <p className="text-gray-600 dark:text-gray-300">
                  Stay updated on player injuries affecting fantasy value
                </p>
              </div>
              <div className="border border-green-500 rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 dark:text-white mb-2">💎 Sleeper Picks</h4>
                <p className="text-gray-600 dark:text-gray-300">
                  Undervalued players with high upside potential
                </p>
              </div>
            </div>
          </div>
        );
      case 'predictions':
        return (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
            <h3 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
              Outcome Predictions
            </h3>
            <div className="space-y-4">
              <div className="bg-gradient-to-r from-purple-50 to-purple-100 dark:from-gray-700 dark:to-gray-600 rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 dark:text-white mb-2">AI-Powered Predictions</h4>
                <p className="text-gray-600 dark:text-gray-300">
                  Machine learning models analyze historical data to predict game outcomes
                </p>
              </div>
              <div className="bg-gradient-to-r from-indigo-50 to-indigo-100 dark:from-gray-700 dark:to-gray-600 rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 dark:text-white mb-2">Confidence Scores</h4>
                <p className="text-gray-600 dark:text-gray-300">
                  Each prediction includes a confidence rating based on data quality and model accuracy
                </p>
              </div>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <button
          onClick={() => navigate('/')}
          className="text-blue-600 dark:text-blue-400 hover:underline mb-4 inline-flex items-center"
        >
          ← Back to Sports
        </button>
        <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-2">
          {sportName} Dashboard
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Comprehensive analytics and insights
        </p>
      </div>

      <div className="mb-6">
        <div className="flex flex-wrap gap-2 border-b border-gray-300 dark:border-gray-600">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 font-medium transition-colors duration-200 ${
                activeTab === tab.id
                  ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.name}
            </button>
          ))}
        </div>
      </div>

      <div className="mb-8">
        {renderTabContent()}
      </div>

      <div className="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500 p-4 rounded">
        <h4 className="font-semibold text-yellow-800 dark:text-yellow-300 mb-2">
          🚧 API Integration Required
        </h4>
        <p className="text-yellow-700 dark:text-yellow-400">
          This is a scaffold version. To enable live data, integrate with public sports APIs such as:
        </p>
        <ul className="list-disc list-inside text-yellow-700 dark:text-yellow-400 mt-2">
          <li>ESPN API - For statistics and scores</li>
          <li>SportsData.io - For comprehensive sports data</li>
          <li>The Odds API - For betting lines and spreads</li>
          <li>SportRadar API - For real-time data</li>
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
