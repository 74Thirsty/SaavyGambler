# StatTracker Pro

A modern, responsive web application for tracking sports statistics and predicting outcomes. Built with React, TypeScript, and Tailwind CSS.

## 🏆 Features

- **Multi-Sport Support**: Track statistics for NFL, NBA, MLB, NHL, Soccer, and MMA/UFC
- **Statistics Dashboard**: Real-time player and team statistics
- **Point Spread Analysis**: Advanced algorithms to predict point spreads and betting lines
- **Fantasy Sports Insights**: Data-driven recommendations to optimize fantasy teams
- **Outcome Predictions**: AI-powered game outcome predictions with confidence scores
- **Modern UI**: Beautiful, responsive interface built with Tailwind CSS
- **API-Ready**: Structured service layer ready for integration with public sports APIs

## 🚀 Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/74Thirsty/stattrackerpro.git
cd stattrackerpro
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

## 📁 Project Structure

```
stattrackerpro/
├── src/
│   ├── components/     # Reusable React components
│   ├── pages/         # Page components (Home, Dashboard)
│   ├── services/      # API service layer
│   ├── types/         # TypeScript type definitions
│   ├── App.tsx        # Main application component
│   ├── main.tsx       # Application entry point
│   └── index.css      # Global styles with Tailwind
├── public/            # Static assets
├── index.html         # HTML template
└── package.json       # Project dependencies
```

## 🔌 API Integration

The application is structured to easily integrate with public sports APIs. Update the API service layer in `src/services/api.ts` to connect to your preferred data sources:

### Recommended APIs

- **ESPN API**: Free sports statistics and scores
  - Base URL: `https://site.web.api.espn.com/apis/site/v2/sports/`
  
- **The Odds API**: Betting odds and spreads
  - Website: https://the-odds-api.com/
  
- **SportsData.io**: Comprehensive sports data
  - Website: https://sportsdata.io/
  
- **SportRadar**: Real-time sports data
  - Website: https://developer.sportradar.com/

### Environment Variables

Create a `.env` file in the root directory to store API keys:

```env
VITE_API_BASE_URL=https://your-api-endpoint.com
VITE_API_KEY=your-api-key
```

## 🛠️ Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

## 🎨 Customization

### Adding a New Sport

1. Edit `src/pages/Home.tsx` and add your sport to the `sports` array
2. Update the dashboard logic in `src/pages/Dashboard.tsx` if needed
3. Add sport-specific types in `src/types/index.ts`

### Styling

The application uses Tailwind CSS for styling. Customize the theme in `tailwind.config.js`:

```javascript
export default {
  theme: {
    extend: {
      colors: {
        // Add custom colors
      }
    }
  }
}
```

## 📊 Data Flow

1. User selects a sport from the home page
2. Application navigates to the sport-specific dashboard
3. Dashboard tabs allow switching between different analysis views:
   - Statistics: Team and player stats
   - Point Spread: Betting line analysis
   - Fantasy: Fantasy sports insights
   - Predictions: Outcome predictions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🔮 Future Enhancements

- [ ] Real-time data integration with sports APIs
- [ ] User authentication and personalized dashboards
- [ ] Historical data visualization with charts
- [ ] Mobile app version
- [ ] Advanced machine learning predictions
- [ ] Live game tracking and notifications
- [ ] Social features for sharing predictions

## 📞 Support

For issues and questions, please open an issue on GitHub.
