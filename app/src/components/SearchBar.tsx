import React, { useState } from 'react';

interface SearchBarProps {
    onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSearch(query);
    };

    return (
        <form onSubmit={handleSubmit} className="w-full max-w-lg">
            <div className="flex items-center rounded-md overflow-hidden p-1">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="w-full px-6 py-3 bg-gray-900 text-cyan-300 border-blue-500 focus:outline-none rounded-md mr-2"
                    placeholder="Search"
                />
                <button
                    type="submit"
                    className="px-6 py-3 bg-blue-500 hover:bg-blue-700 text-white font-bold rounded-md focus:outline-none transition-all duration-300 hover:shadow-neon"
                >
                    Search
                </button>
            </div>
        </form>
    );
};

export default SearchBar;