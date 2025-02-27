import { useState, useEffect, useRef, Dispatch, SetStateAction } from 'react';
import { Send, MessageSquare, Github, Archive, Menu, X, Sun, Moon } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeProvider';

interface HeaderProps {
  onSubscribeClick: () => void;
  onDiscordClick: () => void;
  activeButton: ActiveButton;
  setActiveButton: Dispatch<SetStateAction<ActiveButton>>;
}

interface GitHubStats {
  stars: number;
  forks: number;
}

type ActiveButton = 'subscribe' | 'discord' | 'archive' | 'github' | 'theme';

export const Header: React.FC<HeaderProps> = ({ 
  onSubscribeClick, 
  onDiscordClick, 
  activeButton, 
  setActiveButton 
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [githubStats, setGithubStats] = useState<GitHubStats>({ stars: 0, forks: 0 });
  const { theme, toggleTheme } = useTheme();
  const menuRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const navigate = useNavigate();

  useEffect(() => {
    fetch('https://api.github.com/repos/AICrafterZheng/AI-Frontiers-Digest')
      .then((response) => response.json())
      .then((data) => {
        setGithubStats({
          stars: data.stargazers_count,
          forks: data.forks_count,
        });
      })
      .catch((error) => {
        console.error('Error fetching GitHub stats:', error);
      });
  }, []);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        isMenuOpen &&
        menuRef.current &&
        buttonRef.current &&
        !menuRef.current.contains(event.target as Node) &&
        !buttonRef.current.contains(event.target as Node)
      ) {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isMenuOpen]);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const onArchiveClick = () => {
    navigate('/archive');
  };

  const handleNavItemClick = (callback?: () => void) => {
    setIsMenuOpen(false);
    if (callback) callback();
  };

  const handleSubscribeClick = () => {
    setActiveButton('subscribe');
    onSubscribeClick();
  };

  const handleDiscordClick = () => {
    setActiveButton('discord');
    onDiscordClick();
  };

  const handleArchiveClick = () => {
    setActiveButton('archive');
    onArchiveClick();
  };

  const handleThemeClick = () => {
    setActiveButton('theme');
    toggleTheme();
  };

  const getButtonClass = (buttonType: ActiveButton) => {
    const baseClass = "flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-2 rounded-lg transition-all duration-300 text-xs sm:text-base";
    const gradientClass = "bg-gradient-to-r from-blue-600 via-purple-600 to-blue-600 hover:from-blue-700 hover:via-purple-700 hover:to-blue-700 text-white animate-gradient bg-[length:200%_auto]";
    const regularClass = "bg-gray-100 hover:bg-gray-200 dark:bg-black dark:hover:bg-gray-900 dark:text-white";
    
    return `${baseClass} ${activeButton === buttonType ? gradientClass : regularClass}`;
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-colors duration-200 ${
        isMenuOpen 
          ? 'bg-white dark:bg-black' 
          : 'bg-white/80 dark:bg-black/80'
      } backdrop-blur-sm border-b border-gray-200 dark:border-gray-800`}
    >
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Link 
            to="/" 
            className="hover:opacity-80 transition-opacity"
            onClick={(e) => {
              e.preventDefault();
              navigate('/', { replace: true });
              window.location.reload();
            }}
          >
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">AI Crafter</h1>
          </Link>
        </div>

        {/* Mobile menu button */}
        <button
          ref={buttonRef}
          onClick={toggleMenu}
          className="md:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-900 transition-colors"
          aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={isMenuOpen}
          data-testid="menu-button"
        >
          {isMenuOpen ? (
            <X className="w-6 h-6 text-gray-600 dark:text-gray-300" />
          ) : (
            <Menu className="w-6 h-6 text-gray-600 dark:text-gray-300" />
          )}
        </button>

        {/* Desktop navigation */}
        <div className="hidden md:flex items-center gap-2 sm:gap-4">
          <button
            data-testid="subscribe-button"
            onClick={handleSubscribeClick}
            className={getButtonClass('subscribe')}
          >
            <Send className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <span>Subscribe</span>
          </button>

          <button
            data-testid="discord-button"
            onClick={handleDiscordClick}
            className={getButtonClass('discord')}
          >
            <MessageSquare className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <span>Discord</span>
          </button>

          <button
            data-testid="archive-button"
            onClick={handleArchiveClick}
            className={getButtonClass('archive')}
          >
            <Archive className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <span>Archive</span>
          </button>

          <a
            data-testid="github-link"
            href="https://github.com/AICrafterZheng/AI-Frontiers-Digest"
            target="_blank"
            rel="noopener noreferrer"
            onClick={() => setActiveButton('github')}
            className={getButtonClass('github')}
          >
            <Github className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <div className="flex items-center gap-2 sm:gap-3 text-xs sm:text-sm">
              <span className="flex items-center gap-1">
                <span>★</span> {githubStats.stars}
              </span>
            </div>
          </a>

          <button
            data-testid="theme-toggle"
            onClick={handleThemeClick}
            className={getButtonClass('theme')}
          >
            {theme === 'dark' ? (
              <Sun className="w-3 h-3 sm:w-4 sm:h-4" />
            ) : (
              <Moon className="w-3 h-3 sm:w-4 sm:h-4" />
            )}
            <span>{theme === 'dark' ? 'Light' : 'Dark'}</span>
          </button>
        </div>

        {/* Mobile navigation */}
        {isMenuOpen && (
          <div ref={menuRef} className="absolute top-full left-0 right-0 bg-white dark:bg-black border-b border-gray-200 dark:border-gray-800 shadow-lg md:hidden">
            <div className="flex flex-col p-4 space-y-4 max-w-6xl mx-auto">
              <button
                data-testid="subscribe-button-mobile"
                onClick={() => {
                  handleNavItemClick(handleSubscribeClick);
                }}
                className={getButtonClass('subscribe')}
              >
                <span>Subscribe</span>
                <Send className="w-4 h-4" />
              </button>

              <button
                data-testid="discord-button-mobile"
                onClick={() => {
                  handleNavItemClick(handleDiscordClick);
                }}
                className={getButtonClass('discord')}
              >
                <span>Discord</span>
                <MessageSquare className="w-4 h-4" />
              </button>

              <button
                data-testid="archive-button-mobile"
                onClick={() => {
                  handleNavItemClick(handleArchiveClick);
                }}
                className={getButtonClass('archive')}
              >
                <span>Archive</span>
                <Archive className="w-4 h-4" />
              </button>

              <a
                data-testid="github-link-mobile"
                href="https://github.com/AICrafterZheng/AI-Frontiers-Digest"
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => {
                  setIsMenuOpen(false);
                  setActiveButton('github');
                }}
                className={getButtonClass('github')}
              >
                <span>GitHub</span>
                <div className="flex items-center gap-2">
                  <span>★ {githubStats.stars}</span>
                  <Github className="w-4 h-4" />
                </div>
              </a>

              <button
                data-testid="theme-toggle-mobile"
                onClick={() => {
                  handleNavItemClick(handleThemeClick);
                }}
                className={getButtonClass('theme')}
              >
                <span>{theme === 'dark' ? 'Light' : 'Dark'}</span>
                {theme === 'dark' ? (
                  <Sun className="w-4 h-4" />
                ) : (
                  <Moon className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};