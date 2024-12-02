import { useState, useEffect, useRef } from 'react';
import { Send, MessageSquare, Github, Archive, Menu, X, Sun, Moon } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeProvider';
import { usePlayerStore } from '../store/usePlayerStore';

interface HeaderProps {
  onSubscribeClick: () => void;
  onDiscordClick: () => void;
}

interface GitHubStats {
  stars: number;
  forks: number;
}

export const Header: React.FC<HeaderProps> = ({ onSubscribeClick, onDiscordClick }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [githubStats, setGithubStats] = useState<GitHubStats>({ stars: 0, forks: 0 });
  const { theme, toggleTheme } = useTheme();
  const { close } = usePlayerStore();
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

  return (
    <header className={`fixed top-0 left-0 right-0 backdrop-blur-md z-50 border-b border-gray-200 dark:border-gray-800 transition-colors ${
      isMenuOpen 
        ? 'bg-white dark:bg-gray-900' 
        : 'bg-white/80 dark:bg-gray-900/80'
    }`}>
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Link 
            to="/" 
            className="hover:opacity-80 transition-opacity"
            onClick={close}
          >
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">AI Frontiers</h1>
          </Link>
        </div>

        {/* Mobile menu button */}
        <button
          ref={buttonRef}
          onClick={toggleMenu}
          className="md:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={isMenuOpen}
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
            onClick={onSubscribeClick}
            className="flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-2 rounded-lg bg-[#5865F2] text-white hover:bg-[#4752C4] transition-colors text-xs sm:text-base"
          >
            <Send className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <span>Subscribe</span>
          </button>

          <button
            onClick={onDiscordClick}
            className="flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors text-xs sm:text-base dark:text-white"
          >
            <MessageSquare className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <span>Discord</span>
          </button>

          <button
            onClick={onArchiveClick}
            className="flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors text-xs sm:text-base dark:text-white"
          >
            <Archive className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <span>Archive</span>
          </button>

          <a
            href="https://github.com/AICrafterZheng/AI-Frontiers-Digest"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 sm:gap-3 px-2 sm:px-4 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors text-xs sm:text-base dark:text-white"
          >
            <Github className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <div className="flex items-center gap-2 sm:gap-3 text-xs sm:text-sm">
              <span className="flex items-center gap-1">
                <span>★</span> {githubStats.stars}
              </span>
            </div>
          </a>

          <button
            onClick={toggleTheme}
            className="flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors text-xs sm:text-base dark:text-white"
          >
            <span>{theme === 'dark' ? 'Light' : 'Dark'}</span>
            {theme === 'dark' ? (
              <Sun className="w-3 h-3 sm:w-4 sm:h-4" />
            ) : (
              <Moon className="w-3 h-3 sm:w-4 sm:h-4" />
            )}
          </button>
        </div>

        {/* Mobile navigation */}
        {isMenuOpen && (
          <div ref={menuRef} className="absolute top-full left-0 right-0 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 shadow-lg md:hidden">
            <div className="flex flex-col p-4 space-y-4 max-w-6xl mx-auto">
              <button
                onClick={() => handleNavItemClick(onSubscribeClick)}
                className="flex items-center justify-between px-4 py-3 rounded-lg bg-[#5865F2] text-white hover:bg-[#4752C4] transition-colors"
              >
                <span>Subscribe</span>
                <Send className="w-4 h-4" />
              </button>

              <button
                onClick={() => handleNavItemClick(onDiscordClick)}
                className="flex items-center justify-between px-4 py-3 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors dark:text-white"
              >
                <span>Discord</span>
                <MessageSquare className="w-4 h-4" />
              </button>

              <button
                onClick={() => handleNavItemClick(onArchiveClick)}
                className="flex items-center justify-between px-4 py-3 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors dark:text-white"
              >
                <span>Archive</span>
                <Archive className="w-4 h-4" />
              </button>

              <a
                href="https://github.com/AICrafterZheng/AI-Frontiers-Digest"
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => setIsMenuOpen(false)}
                className="flex items-center justify-between px-4 py-3 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors dark:text-white"
              >
                <span>GitHub</span>
                <div className="flex items-center gap-2">
                  <span>★ {githubStats.stars}</span>
                  <Github className="w-4 h-4" />
                </div>
              </a>

              <button
                onClick={toggleTheme}
                className="flex items-center justify-between px-4 py-3 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors dark:text-white"
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