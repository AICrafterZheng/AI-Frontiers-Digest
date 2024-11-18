interface NewsEntryProps {
  title: string;
  date: string;
  summary: string;
}

export default function NewsEntry({ title, date, summary }: NewsEntryProps) {
  return (
    <article className="border-b border-gray-200 py-6 hover:bg-gray-50 transition-colors">
      <div className="flex justify-between items-start gap-4">
        <div className="space-y-2">
          <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
          <p className="text-gray-600 line-clamp-2">{summary}</p>
        </div>
        <time className="text-gray-500 whitespace-nowrap">{date}</time>
      </div>
    </article>
  );
} 