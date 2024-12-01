import { useNavigate } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';

interface NewsCategoryProps {
  title: string;
  icon: React.ReactNode;
  lastUpdate: string;
  backgroundColor: string;
  items: {
    id: number;
    title: string;
    points?: number;
    stars?: number;
    slug?: string;  // for URL routing
  }[];
}

export default function NewsCategory({ title, icon, lastUpdate, backgroundColor, items }: NewsCategoryProps) {
  const navigate = useNavigate();

  const handleItemClick = (id: number, slug?: string) => {
    navigate(`/article/${slug || id}`);
  };

  return (
    <div className={`rounded-xl p-4 ${backgroundColor} dark:bg-opacity-90`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          {icon}
          <h2 className="text-white font-semibold">{title}</h2>
        </div>
        <div className="text-white/70 text-sm">{lastUpdate}</div>
      </div>
      
      <div className="space-y-3">
        {items.map((item) => (
          <button
            key={item.id}
            onClick={() => handleItemClick(item.id, item.slug)}
            className="w-full flex items-start gap-3 hover:bg-white/10 dark:hover:bg-white/5 p-2 rounded-lg transition-colors text-left"
          >
            <span className="text-white/70">{item.id}</span>
            <div className="flex-1">
              <p className="text-white">{item.title}</p>
              <div className="flex items-center gap-2">
                {item.points && <span className="text-white/60 text-sm">{item.points} points</span>}
                {item.stars && <span className="text-white/60 text-sm">★ {item.stars}</span>}
              </div>
            </div>
            <ChevronRight className="w-4 h-4 text-white/40" />
          </button>
        ))}
      </div>
    </div>
  );
} 