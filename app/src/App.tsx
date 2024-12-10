import { useState } from 'react';
import SearchBar from './components/SearchBar';
import ImageGrid from './components/ImageGrid';
import './tailwind.css'

interface SearchResult {
    text_query: string;
    image_list_with_metadata: Array<{
        image_path: string;
        application_name: string;
        timestamp: string;
        distance: number;
    }>;
}

function App() {
    const [searchResults, setSearchResults] = useState<SearchResult | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSearch = async (query: string) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await fetch(`http://127.0.0.1:8000/search?text_query=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error('Failed to fetch search results');
            }
            const data: SearchResult = await response.json();
            setSearchResults(data);
        } catch (error) {
            console.error('Error fetching search results:', error);
            setError('An error occurred while fetching results. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-black text-gray-200 font-geist flex flex-col items-center justify-center p-4">
            <h1 className="text-6xl font-bold mb-8 text-blue-500">smarn</h1>
            <div className="max-w-4xl mb-8">
                <SearchBar onSearch={handleSearch} />
            </div>
            {isLoading && (
                <div className="text-center text-gray-400">Loading...</div>
            )}
            {error && (
                <div className="text-center text-red-400">{error}</div>
            )}
            {searchResults && (
                <ImageGrid images={searchResults.image_list_with_metadata} />
            )}
        </div>
    );
}

export default App;