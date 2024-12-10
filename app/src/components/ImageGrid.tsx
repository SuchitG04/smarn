import React, { useState } from 'react';
import ImageViewer from './ImageViewer';
import Image from './Image';

interface ImageMetadata {
    image_path: string;
    application_name: string;
    timestamp: string;
}

interface ImageGridProps {
    images: ImageMetadata[];
}

const ImageGrid: React.FC<ImageGridProps> = ({ images }) => {
    const [selectedImageIndex, setSelectedImageIndex] = useState<number | null>(null);

    const handleImageClick = (index: number) => {
        setSelectedImageIndex(index);
    };

    const handleCloseViewer = () => {
        setSelectedImageIndex(null);
    };

    if (images.length === 0) {
        return (
            <div className="text-center text-gray-400 mt-8">
                No results found. Please try a different search query.
            </div>
        );
    }

    return (
        <>
            <div className="w-3/4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {images.map((image, index) => (
                    <div
                        key={index}
                        className="bg-gray-900 rounded-md overflow-hidden shadow-md transition-transform duration-200 hover:scale-105 cursor-pointer"
                        onClick={() => handleImageClick(index)}
                    >
                        <Image
                            imagePath={image.image_path}
                            alt={`Screenshot from ${image.application_name}`}
                            className="w-full h-48 object-cover"
                        />
                        <div className="p-4">
                            <h3 className="text-gray-300 font-medium">{image.application_name}</h3>
                            <p className="text-gray-500 text-sm mt-1">{image.timestamp}</p>
                        </div>
                    </div>
                ))}
            </div>
            {selectedImageIndex !== null && (
                <ImageViewer
                    images={images.map(img => img.image_path)}
                    initialIndex={selectedImageIndex}
                    onClose={handleCloseViewer}
                />
            )}
        </>
    );
};

export default ImageGrid;