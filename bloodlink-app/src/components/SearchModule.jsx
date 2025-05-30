// src/components/SearchModule.jsx
import React, { useState } from 'react';
import { db, appId } from '../firebaseConfig';
import { collection, query, where, getDocs } from 'firebase/firestore';

function SearchModule({
    setSearchResults,
    setCurrentPage,
    setError,
    setLoading,
    setSearchCriteria,
    bloodGroups,
    setSuccessMessage // <-- ADDED PROP
}) {
    const [bloodType, setBloodType] = useState(bloodGroups[0]);
    const [city, setCity] = useState('');

    const handleSearch = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccessMessage(''); // Clear previous success/info messages
        setSearchResults([]);

        if (!bloodType) {
            setError("Please select a blood type.");
            setLoading(false);
            return;
        }
        if (!city.trim()) {
            setError("Please enter a city name.");
            setLoading(false);
            return;
        }

        const trimmedCity = city.trim();
        setSearchCriteria({ bloodType, city: trimmedCity });

        try {
            const donorsRef = collection(db, `/artifacts/${appId}/public/data/donors`);
            const q = query(donorsRef, where("bloodType", "==", bloodType), where("city", "==", trimmedCity));
            
            const querySnapshot = await getDocs(q);
            const results = [];
            querySnapshot.forEach((doc) => {
                results.push({ id: doc.id, ...doc.data() });
            });

            if (results.length === 0) {
                // Use setSuccessMessage for informational messages like "no results"
                // Or setError if you want it styled as an error.
                // For consistency with other error/success messages, let's use setSuccessMessage
                // or you could introduce a new state for 'infoMessage'.
                setSuccessMessage(`No donors found for ${bloodType} in ${trimmedCity}. Try a different search.`);
            } else {
                 setSuccessMessage(''); // Clear if results are found
            }
            setSearchResults(results);
            setCurrentPage('results');
        } catch (err) {
            console.error("Error searching donors:", err);
            setError('Search failed: ' + (err.message || "An unexpected error occurred.") + ". Please check Firestore security rules or try again later.");
        }
        setLoading(false);
    };

    return (
        <div className="max-w-md mx-auto bg-white p-6 sm:p-8 rounded-xl shadow-2xl">
            <h2 className="text-2xl sm:text-3xl font-bold text-center text-red-700 mb-6">Find a Blood Donor</h2>
            <form onSubmit={handleSearch} className="space-y-4">
                <div>
                    <label htmlFor="bloodTypeSearch" className="block text-sm font-medium text-gray-700">Blood Type Needed</label>
                    <select 
                        id="bloodTypeSearch"
                        value={bloodType} 
                        onChange={(e) => setBloodType(e.target.value)}
                        // Added text-gray-900 to ensure select text is dark
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 text-gray-900"
                    >
                        {bloodGroups.map(bg => 
                            // Added text-black to option tags for explicit dark text
                            <option key={bg} value={bg} className="text-black">{bg}</option>
                        )}
                    </select>
                </div>
                <div>
                    <label htmlFor="citySearch" className="block text-sm font-medium text-gray-700">City</label>
                    <input 
                        id="citySearch"
                        type="text" 
                        value={city} 
                        onChange={(e) => setCity(e.target.value)} 
                        placeholder="Enter city name" 
                        required
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500" 
                    />
                </div>
                <button 
                    type="submit"
                    className="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
                >
                    Search Donors
                </button>
            </form>
        </div>
    );
}

export default SearchModule;
