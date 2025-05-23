import { X } from 'lucide-react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

export default function Modal({ isOpen, onClose, children }: ModalProps) {
  if (!isOpen) return null;

  return (
    <>
      {/* Portal container for modal */}
      <div className="fixed inset-0 z-[9999] overflow-y-auto">
        <div className="flex min-h-full items-center justify-center p-4">
          {/* Overlay */}
          <div 
            className="fixed inset-0 bg-black/50 transition-opacity" 
            onClick={onClose}
            aria-hidden="true"
          />

          {/* Modal panel */}
          <div className="relative z-[10000] w-full max-w-lg transform rounded-lg bg-white dark:bg-black text-gray-900 dark:text-white shadow-xl transition-all">
            <button
              onClick={onClose}
              className="absolute right-2 top-2 p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
            >
              <X className="w-5 h-5" />
            </button>
            {children}
          </div>
        </div>
      </div>
    </>
  );
} 