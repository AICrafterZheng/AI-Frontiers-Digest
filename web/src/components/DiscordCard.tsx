import { MessageSquare, Check } from 'lucide-react';
import { DISCORD_SERVER_INVITE } from '../utils/constants';

export function DiscordCard() {
  return (
    <div className="bg-white rounded-3xl p-8 text-gray-900 shadow-lg">
      <div className="flex items-center gap-3 mb-4">
        <MessageSquare className="w-6 h-6 text-[#5865F2]" />
        <h2 className="text-2xl font-semibold">Discord Community</h2>
      </div>
      <p className="text-gray-600 mb-8">
        Join our vibrant Discord community to connect, share, and grow with fellow members.
      </p>
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-4">What you'll get:</h3>
        <ul className="space-y-3">
          {[
            'Exclusive community events',
            'Direct access to our team',
            'Networking opportunities'
          ].map((benefit, index) => (
            <li key={index} className="flex items-center gap-3">
              <Check className="w-5 h-5 text-[#5865F2]" />
              <span className="text-gray-600">{benefit}</span>
            </li>
          ))}
        </ul>
      </div>
      <a
        href={DISCORD_SERVER_INVITE}
        target="_blank"
        rel="noopener noreferrer"
        className="block w-full bg-[#5865F2] text-white font-semibold py-3 px-6 rounded-xl hover:bg-[#4752C4] transition-colors text-center flex items-center justify-center gap-2"
      >
        <MessageSquare className="w-5 h-5" />
        Join Discord
      </a>
    </div>
  );
}