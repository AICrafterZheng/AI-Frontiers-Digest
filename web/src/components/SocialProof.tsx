export function SocialProof() {
  return (
    <div className="mt-20 text-center">
      <p className="text-gray-600 mb-8">Trusted by developers from</p>
      <div className="flex justify-center space-x-12 opacity-50">
        <img
          src="https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=80&h=40&fit=crop&auto=format"
          alt="Company 1"
          className="h-8 w-auto"
        />
        <img
          src="https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=80&h=40&fit=crop&auto=format"
          alt="Company 2"
          className="h-8 w-auto"
        />
        <img
          src="https://images.unsplash.com/photo-1611162618071-b39a2ec055fb?w=80&h=40&fit=crop&auto=format"
          alt="Company 3"
          className="h-8 w-auto"
        />
      </div>
    </div>
  );
}