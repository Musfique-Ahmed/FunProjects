// src/components/SearchModule.jsx
import React, { useState } from 'react';
// Import db, appId, and Firebase query functions
import { db, appId } from '../firebaseConfig'; // Assuming firebaseConfig.js is in src/
import { collection, query, where, getDocs } from 'firebase/firestore';

function SearchModule({
    setSearchResults,
    setCurrentPage,
    setError,
    setLoading,
    setSearchCriteria,
    bloodGroups // Prop received from App.jsx
}) {
    const [bloodType, setBloodType] = useState(bloodGroups[0]);
    const [city, setCity] = useState('');

    const handleSearch = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSearchResults([]); // Clear previous results

        if (!bloodType) { // City is also required by the form's `required` attribute
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
            // Firestore Security Rules Reminder:
            // Ensure your rules for `/artifacts/{appId}/public/data/donors` allow read access for this query.
            // e.g., `match /artifacts/{appId}/public/data/donors/{donorId} { allow read: if true; }`
            // or `match /artifacts/{appId}/public/data/donors/{donorId} { allow list: if true; }` on the collection.
            // For case-insensitive city search, you'd typically store a lowercase version of city in Firestore
            // and query against that: `where("city_lowercase", "==", trimmedCity.toLowerCase())`.
            // This example uses an exact match for simplicity.

            const donorsRef = collection(db, `/artifacts/${appId}/public/data/donors`);
            const q = query(donorsRef, where("bloodType", "==", bloodType), where("city", "==", trimmedCity));
            
            const querySnapshot = await getDocs(q);
            const results = [];
            querySnapshot.forEach((doc) => {
                results.push({ id: doc.id, ...doc.data() });
            });

            if (results.length === 0) {
                setSuccessMessage(`No donors found for ${bloodType} in ${trimmedCity}. Try a different search.`);
            } else {
                 setSuccessMessage(''); // Clear any previous no results message
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
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500"
                    >
                        {bloodGroups.map(bg => <option key={bg} value={bg}>{bg}</option>)}
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
