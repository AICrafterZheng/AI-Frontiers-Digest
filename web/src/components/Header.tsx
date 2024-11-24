import { useState, useEffect } from 'react';
import { Send, MessageSquare, Github, Archive } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';

interface GitHubStats {
  stars: number;
  forks: number;
}

// Add this interface to define the props
interface HeaderProps {
  onSubscribeClick: () => void;
  onDiscordClick: () => void;
}

// Update the component declaration to use the props interface
export const Header: React.FC<HeaderProps> = ({ onSubscribeClick, onDiscordClick }) => {
  const [githubStats, setGithubStats] = useState<GitHubStats>({ stars: 0, forks: 0 });

  const navigate = useNavigate();
  const onArchiveClick = () => {
    navigate(`/archive`);
  };

  useEffect(() => {
    // Replace with your GitHub repo details
    const owner = 'AICrafterZheng';
    const repo = 'AI-Frontiers-Digest';
    
    fetch(`https://api.github.com/repos/${owner}/${repo}`)
      .then(res => res.json())
      .then(data => {
        setGithubStats({
          stars: data.stargazers_count,
          forks: data.forks_count
        });
      })
      .catch(console.error);
  }, []);

  return (
    <header className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md z-50 border-b border-gray-200">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Link to="/" className="hover:opacity-80 transition-opacity">
            <h1 className="text-xl font-bold text-gray-900">AI Frontiers</h1>
          </Link>
        </div>

        <div className="flex items-center gap-2 sm:gap-4">
          <button
            onClick={onSubscribeClick}
            className="flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-2 rounded-lg bg-[#5865F2] text-white hover:bg-[#4752C4] transition-colors text-xs sm:text-base"
          >
            <Send className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <span>Subscribe</span>
          </button>

          <button
            onClick={onDiscordClick}
            className="flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-2 rounded-lg bg-[#5865F2] text-white hover:bg-[#4752C4] transition-colors text-xs sm:text-base"
          >
            <MessageSquare className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <span>Discord</span>
          </button>

          <button
            onClick={onArchiveClick}
            className="flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors text-xs sm:text-base"
          >
            <Archive className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <span>Archive</span>
          </button>

          <a
            href="https://github.com/AICrafterZheng/AI-Frontiers-Digest"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 sm:gap-3 px-2 sm:px-4 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors text-xs sm:text-base"
          >
            <Github className="w-3 h-3 sm:w-4 sm:h-4 hidden sm:block" />
            <div className="flex items-center gap-2 sm:gap-3 text-xs sm:text-sm">
              <span className="flex items-center gap-1">
                <span>★</span> {githubStats.stars}
              </span>
              {/* <span className="flex items-center gap-1">
                <span>𝝙</span> {githubStats.forks}
              </span> */}
            </div>
          </a>
        </div>
      </div>
    </header>
  );
}