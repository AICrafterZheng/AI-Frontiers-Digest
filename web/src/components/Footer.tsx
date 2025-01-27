import React from 'react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white dark:bg-black mt-auto">
      <div className="max-w-screen-xl mx-auto px-4 py-8">
        <div className="flex flex-col items-center space-y-6">
          <div className="flex flex-wrap justify-center items-center gap-8 text-gray-500 dark:text-gray-400">
          <span className="text-sm text-gray-500 dark:text-gray-400">
            Built with ❤️ by{' '}
            <a
              href="https://dannyzheng.me"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:underline text-blue-600 dark:text-blue-500"
            >
              dannyzheng.me
            </a>
          </span>
            <a href="/feedback" className="hover:text-gray-900 dark:hover:text-white transition-colors">
              Feedback
            </a>
            <a
              href="https://x.com/dannyzhengme"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-gray-900 dark:hover:text-white transition-colors"
            >
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="currentColor">
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
            </svg>
            </a>
          </div>
          
          <span className="text-sm text-gray-500 dark:text-gray-400">
          &copy;{currentYear} AI Frontiers. All Rights Reserved.
          </span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
