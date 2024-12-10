import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, X } from 'lucide-react';
import Image from './Image';

interface ImageViewerProps {
    images: string[];
    initialIndex: number;
    onClose: () => void;
}

const ImageViewer: React.FC<ImageViewerProps> = ({ images, initialIndex, onClose }) => {
    const [currentIndex, setCurrentIndex] = useState(initialIndex);

    const handlePrev = () => setCurrentIndex((prev) => (prev > 0 ? prev - 1 : images.length - 1));
    const handleNext = () => setCurrentIndex((prev) => (prev < images.length - 1 ? prev + 1 : 0));

    return (
        <div className="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50">
            <div className="relative w-full h-full flex items-center justify-center">
                <Image
                    imagePath={images[currentIndex]}
                    alt={`Image ${currentIndex + 1}`}
                    className="max-w-full max-h-full object-contain"
                />
                <button
                    onClick={handlePrev}
                    className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-blue-500 text-white p-3 rounded-full transition-all duration-300 hover:scale-110 hover:shadow-neon"
                >
                    <ChevronLeft size={24} />
                </button>
                <button
                    onClick={handleNext}
                    className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-blue-500 text-white p-3 rounded-full transition-all duration-300 hover:scale-110 hover:shadow-neon"
                >
                    <ChevronRight size={24} />
                </button>
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 bg-blue-500 text-white p-3 rounded-full transition-all duration-300 hover:scale-110 hover:shadow-neon"
                >
                    <X size={24} />
                </button>
            </div>
        </div>
    );
};

export default ImageViewer;