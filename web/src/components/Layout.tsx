import { Header } from './Header';
import { Outlet } from 'react-router-dom';
import { useState } from 'react';
import Modal from "./Modal"
import { SubscribeNewsletterCard } from './SubNewsletterCard';
import { DiscordCard } from './DiscordCard';
import { Player } from './Player';
import Footer from './Footer';

export default function Layout() {
  const [showSubscribe, setShowSubscribe] = useState(false);
  const [showDiscord, setShowDiscord] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800 text-gray-900 dark:text-gray-100 flex flex-col">
      <Header 
        onSubscribeClick={() => setShowSubscribe(true)}
        onDiscordClick={() => setShowDiscord(true)}
      />
      
      <main className="relative pt-24 px-4 pb-32 flex-grow">
        <div className="max-w-6xl mx-auto">
          <Outlet />
        </div>
      </main>

      {/* Player */}
      <Player />

      {/* Footer */}
      <Footer />

      {/* Modals */}
      <Modal isOpen={showSubscribe} onClose={() => setShowSubscribe(false)}>
        <SubscribeNewsletterCard />
      </Modal>

      <Modal isOpen={showDiscord} onClose={() => setShowDiscord(false)}>
        <DiscordCard />
      </Modal>
    </div>
  );
}