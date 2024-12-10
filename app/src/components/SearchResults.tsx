import React from 'react';
import SearchBar from './SearchBar';
import ImageGrid from './ImageGrid';

interface SearchResultsProps {
    results: any;
    onSearch: (query: string) => void;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results, onSearch }) => {
    return (
        <div className="flex flex-col items-center w-full bg-gray-900 min-h-screen">
            <div className="max-w-4xl w-full mb-12 mt-8">
                <h1 className="text-4xl font-bold text-center mb-8 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
                    Awesome Image Search
                </h1>
                <SearchBar onSearch={onSearch} />
            </div>
            <div className="max-w-7xl w-full px-4">
                <ImageGrid images={results.image_list_with_metadata} />
            </div>
        </div>
    );
};

export default SearchResults;