import React, { useState, useEffect } from 'react';

interface ImageProps {
    imagePath: string;
    alt: string;
    className?: string;
}

const Image: React.FC<ImageProps> = ({ imagePath, alt, className }) => {
    const [imageUrl, setImageUrl] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchImage = async () => {
            try {
                const imageName = imagePath.split('/').pop();
                const response = await fetch(`http://localhost:8000/images/${imageName}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch image');
                }
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                setImageUrl(url);
            } catch (err) {
                console.error('Error fetching image:', err);
                setError('Failed to load image');
            }
        };

        fetchImage();

        return () => {
            if (imageUrl) {
                URL.revokeObjectURL(imageUrl);
            }
        };
    }, [imagePath]);

    if (error) {
        return <div className={`bg-gradient-to-r from-red-500 to-pink-500 flex items-center justify-center ${className} rounded-lg text-white font-bold`}>{error}</div>;
    }

    return (
        <>
            {imageUrl ? (
                <img
                    src={imageUrl}
                    alt={alt}
                    className={`${className} cursor-pointer rounded-lg transform transition-all duration-300 hover:scale-105 hover:shadow-neon`}
                />
            ) : (
                <div className={`bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center ${className} rounded-lg text-white font-bold animate-pulse`}>Loading...</div>
            )}
        </>
    );
};

export default Image;