import React from 'react';
import { FaTwitter } from 'react-icons/fa';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white dark:bg-gray-900 mt-auto">
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
            <a href="https://aicrafter.canny.io/feature-requests" className="hover:text-gray-900 dark:hover:text-white transition-colors">
              Feedback
            </a>
            <a
              href="https://x.com/dannyzhengme"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              <FaTwitter className="w-5 h-5" />
            </a>
          </div>
          
          <span className="text-sm text-gray-500 dark:text-gray-400">
          ©{currentYear} AI Frontiers. All Rights Reserved.
          </span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
