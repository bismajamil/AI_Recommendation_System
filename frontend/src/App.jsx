import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [preferences, setPreferences] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [customInterest, setCustomInterest] = useState('');

  const categories = ['python', 'movies', 'ai', 'data-science', 'programming'];

  const togglePreference = (category) => {
    setPreferences(prev =>
      prev.includes(category)
        ? prev.filter(p => p !== category)
        : [...prev, category]
    );
  };

  const addCustomInterest = () => {
    if (customInterest.trim() === '') {
      setError('Please enter an interest');
      return;
    }
    
    const newInterest = customInterest.toLowerCase().trim();
    if (preferences.includes(newInterest)) {
      setError('This interest is already added');
      return;
    }
    
    setPreferences([...preferences, newInterest]);
    setCustomInterest('');
    setError('');
  };

  const removePreference = (pref) => {
    setPreferences(preferences.filter(p => p !== pref));
  };

  const getRecommendations = async () => {
    if (preferences.length === 0) {
      setError('Please select at least one preference');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5000/api/recommendations', {
        preferences: preferences
      });
      setRecommendations(response.data.recommendations);
    } catch (err) {
      setError('Failed to get recommendations. Make sure backend is running!');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="app-wrapper">
        <h1 className="title">🎯 Recommendation System</h1>
        <p className="subtitle">Select your interests to get personalized recommendations</p>

        {/* Preference Selector */}
        <div className="preference-section">
          <h2>Select Your Interests</h2>
          <div className="preference-buttons">
            {categories.map(category => (
              <button
                key={category}
                className={`preference-btn ${preferences.includes(category) ? 'active' : ''}`}
                onClick={() => togglePreference(category)}
              >
                {category.charAt(0).toUpperCase() + category.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Custom Interest Input */}
        <div className="custom-interest-section">
          <h2>Add Your Own Interest</h2>
          <div className="custom-input-group">
            <input
              type="text"
              className="custom-input"
              placeholder="e.g., gaming, music, sports..."
              value={customInterest}
              onChange={(e) => setCustomInterest(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && addCustomInterest()}
            />
            <button className="add-btn" onClick={addCustomInterest}>
              + Add
            </button>
          </div>
        </div>

        {/* Selected Preferences Display */}
        {preferences.length > 0 && (
          <div className="selected-preferences">
            <h3>Your Interests ({preferences.length})</h3>
            <div className="preference-tags">
              {preferences.map(pref => (
                <div key={pref} className="preference-tag">
                  <span>{pref.charAt(0).toUpperCase() + pref.slice(1)}</span>
                  <button 
                    className="remove-tag-btn"
                    onClick={() => removePreference(pref)}
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Get Recommendations Button */}
        <button
          className="get-recommendations-btn"
          onClick={getRecommendations}
          disabled={loading || preferences.length === 0}
        >
          {loading ? 'Loading...' : 'Get Recommendations'}
        </button>

        {/* Error Message */}
        {error && <div className="error-message">{error}</div>}

        {/* Recommendations Display */}
        {recommendations.length > 0 && (
          <div className="recommendations-section">
            <h2>✨ Recommended For You</h2>
            <p className="found-count">Found {recommendations.length} recommendations</p>
            <div className="recommendations-grid">
              {recommendations.map(item => (
                <div key={item.id} className="recommendation-card">
                  <div className="card-header">
                    <h3>{item.title}</h3>
                    <span className="type-badge">{item.type}</span>
                  </div>
                  <p className="card-categories">
                    {item.categories.join(', ')}
                  </p>
                  <div className="card-footer">
                    <div className="rating">⭐ {item.rating}</div>
                    <div className="match-score">Match: {(item.matchScore).toFixed(1)}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
