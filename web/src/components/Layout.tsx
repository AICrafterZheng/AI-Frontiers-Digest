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
  const [activeHeaderButton, setActiveHeaderButton] = useState('subscribe');

  const handleCloseSubscribe = () => {
    setShowSubscribe(false);
    setActiveHeaderButton('subscribe');
  };

  const handleCloseDiscord = () => {
    setShowDiscord(false);
    setActiveHeaderButton('subscribe');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-black dark:to-black text-gray-900 dark:text-gray-100 flex flex-col">
      <Header 
        onSubscribeClick={() => setShowSubscribe(true)}
        onDiscordClick={() => setShowDiscord(true)}
        activeButton={activeHeaderButton}
        setActiveButton={setActiveHeaderButton}
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
      <Modal isOpen={showSubscribe} onClose={handleCloseSubscribe}>
        <SubscribeNewsletterCard />
      </Modal>

      <Modal isOpen={showDiscord} onClose={handleCloseDiscord}>
        <DiscordCard />
      </Modal>
    </div>
  );
}