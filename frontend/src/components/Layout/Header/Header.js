import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Header.css';

const Header = ({ isLandingPage = false }) => {
  const navigate = useNavigate();
  const location = useLocation(); 

  const handleExploreClick = () => {
    navigate('/feed');
  };
  const handleHomeClick = () => {
    navigate('/');
  };
  const handleStoriesClick = () => {
    navigate('/feed');
  };
  const handleSubmitClick = () => {
    navigate('/submit');
  };

  const renderNavigation = () => {
    if (isLandingPage) {
      return (
        <button 
          className="header__explore-btn"
          onClick={handleExploreClick}
        >
          Explore Trending Stories
        </button>
      );
    }

    switch (location.pathname) {
      case '/feed':
        return (
          <nav className="header__nav">
            <button className='header__home-btn' onClick={handleHomeClick}>Home</button>
            <button className='header__submit-btn' onClick={handleSubmitClick}>Submit</button>
          </nav>
        );
      
      case '/submit':
        return (
          <nav className="header__nav">
            <button className='header__home-btn' onClick={handleHomeClick}>Home</button>
            <button className='header__stories-btn' onClick={handleStoriesClick}>Stories</button>
          </nav>
        );
      
      default:
        return (
          <nav className="header__nav">
            <button className='header__home-btn' onClick={handleHomeClick}>Home</button>
            <button className='header__stories-btn' onClick={handleStoriesClick}>Stories</button>
          </nav>
        );
    }
  };

  return (
    <header className={`header ${isLandingPage ? 'header--landing' : 'header--feed'}`}>
      <div className="header__container">
        <div className="header__logo" onClick={() => navigate('/')}>
          <h1>BangkokLore</h1>
        </div>
        
        {renderNavigation()}
      </div>
    </header>
  );
};

export default Header;
