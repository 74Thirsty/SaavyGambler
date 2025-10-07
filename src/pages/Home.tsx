import { useNavigate } from 'react-router-dom';

const sports = [
  {
    id: 'nfl',
    name: 'NFL',
    icon: '🏈',
    description: 'National Football League',
    color: 'bg-gradient-to-br from-red-500 to-red-700'
  },
  {
    id: 'nba',
    name: 'NBA',
    icon: '🏀',
    description: 'National Basketball Association',
    color: 'bg-gradient-to-br from-orange-500 to-orange-700'
  },
  {
    id: 'mlb',
    name: 'MLB',
    icon: '⚾',
    description: 'Major League Baseball',
    color: 'bg-gradient-to-br from-blue-500 to-blue-700'
  },
  {
    id: 'nhl',
    name: 'NHL',
    icon: '🏒',
    description: 'National Hockey League',
    color: 'bg-gradient-to-br from-gray-600 to-gray-800'
  },
  {
    id: 'soccer',
    name: 'Soccer',
    icon: '⚽',
    description: 'International Soccer',
    color: 'bg-gradient-to-br from-green-500 to-green-700'
  },
  {
    id: 'mma',
    name: 'MMA/UFC',
    icon: '🥊',
    description: 'Mixed Martial Arts',
    color: 'bg-gradient-to-br from-purple-500 to-purple-700'
  }
];

function Home() {
  const navigate = useNavigate();

  const handleSportSelect = (sportId: string) => {
    navigate(`/dashboard/${sportId}`);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="text-center mb-12">
        <h1 className="text-5xl font-bold text-gray-800 dark:text-white mb-4">
          StatTracker Pro
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300">
          Advanced Sports Analytics & Predictions
        </p>
        <p className="text-md text-gray-500 dark:text-gray-400 mt-2">
          Track statistics, analyze point spreads, optimize fantasy teams, and predict outcomes
        </p>
      </header>

      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-6 text-center">
          Select Your Sport
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {sports.map((sport) => (
            <button
              key={sport.id}
              onClick={() => handleSportSelect(sport.id)}
              className={`${sport.color} text-white p-8 rounded-xl shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 ease-in-out`}
            >
              <div className="text-6xl mb-4">{sport.icon}</div>
              <h3 className="text-2xl font-bold mb-2">{sport.name}</h3>
              <p className="text-sm opacity-90">{sport.description}</p>
            </button>
          ))}
        </div>
      </div>

      <div className="mt-16 max-w-4xl mx-auto">
        <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-6 text-center">
          Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
            <div className="text-4xl mb-4 text-center">📊</div>
            <h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white text-center">
              Statistics Tracking
            </h3>
            <p className="text-gray-600 dark:text-gray-300 text-center">
              Real-time player and team statistics from public APIs
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
            <div className="text-4xl mb-4 text-center">🎯</div>
            <h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white text-center">
              Point Spread Analysis
            </h3>
            <p className="text-gray-600 dark:text-gray-300 text-center">
              Advanced algorithms to predict point spreads and betting lines
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
            <div className="text-4xl mb-4 text-center">🏆</div>
            <h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white text-center">
              Fantasy Insights
            </h3>
            <p className="text-gray-600 dark:text-gray-300 text-center">
              Optimize your fantasy team with data-driven recommendations
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
