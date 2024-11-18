import { Header } from './Header';
import { Outlet } from 'react-router-dom';
import { useState } from 'react';
import Modal from "./Modal"
import { SubscribeNewsletterCard } from './SubNewsletterCard';
import { DiscordCard } from './DiscordCard';

export default function Layout() {
  const [showSubscribe, setShowSubscribe] = useState(false);
  const [showDiscord, setShowDiscord] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
    <Header 
      onSubscribeClick={() => setShowSubscribe(true)}
      onDiscordClick={() => setShowDiscord(true)}
    />
    
    <main className="relative pt-24 px-4 pb-16">
      <div className="max-w-6xl mx-auto">
        <Outlet />
      </div>
    </main>

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