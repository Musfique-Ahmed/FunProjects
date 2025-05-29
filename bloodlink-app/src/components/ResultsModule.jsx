// src/components/ResultsModule.jsx
import React, { useState, useEffect } from 'react'; // Added useEffect for Modal

// Modal component can be defined here or imported if moved to its own file
// For simplicity here, assuming Modal is passed or defined in App.jsx and available globally
// If Modal is defined in App.jsx and not exported, you need to pass it as a prop or redefine it here.
// Let's assume App.jsx passes Modal as a prop or you'll copy its definition here.
// For this example, I'll assume Modal is available (e.g. from App.jsx or a utils file)
// If Modal is defined in App.jsx, you would typically pass it as a prop:
// function ResultsModule({ results, searchCriteria, setCurrentPage, setError, ModalComponent }) 
// Then use <ModalComponent>...</ModalComponent>
// For now, let's copy the Modal definition here as it was in the single App.jsx file.

function Modal({ children, onClose }) {
    useEffect(() => {
        const handleEsc = (event) => {
            if (event.key === 'Escape') {
                onClose();
            }
        };
        window.addEventListener('keydown', handleEsc);
        return () => {
            window.removeEventListener('keydown', handleEsc);
        };
    }, [onClose]);

    return (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm" onClick={onClose}>
            <div className="bg-white p-6 rounded-xl shadow-2xl max-w-lg w-full transform transition-all" onClick={e => e.stopPropagation()}>
                {children}
                <button onClick={onClose} className="mt-6 w-full py-2.5 px-4 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50">
                    Close
                </button>
            </div>
        </div>
    );
}


function ResultsModule({ results, searchCriteria, setCurrentPage, setError }) {
    const [selectedDonor, setSelectedDonor] = useState(null);

    const handleNotifyClick = (donor) => {
        setError(''); // Clear previous errors
        if (donor.wantsNotifications) {
            setSelectedDonor(donor);
        } else {
            // Using setError to display this message, as AlertMessage is handled in App.jsx
            setError("This donor has not consented to be contacted directly. Please respect their privacy.");
            setSelectedDonor(null); 
        }
    };
    
    if (!searchCriteria) {
         return (
            <div className="text-center p-6 bg-white rounded-xl shadow-xl">
                <p className="text-gray-700 text-lg">Please perform a search first to see results.</p>
                <button 
                    onClick={() => setCurrentPage('search')} 
                    className="mt-6 px-6 py-2 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-colors shadow-md hover:shadow-lg"
                >
                    Go to Search Page
                </button>
            </div>
        );
    }

    return (
        <div className="max-w-2xl mx-auto">
            <h2 className="text-2xl sm:text-3xl font-bold text-center text-red-700 mb-6">
                Search Results for {searchCriteria.bloodType} in {searchCriteria.city}
            </h2>
            {results.length === 0 ? (
                <div className="text-center text-gray-600 bg-white p-6 rounded-xl shadow-lg">
                    <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                        <path vectorEffect="non-scaling-stroke" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                    </svg>
                    <h3 className="mt-2 text-lg font-medium text-gray-900">No donors found</h3>
                    <p className="mt-1 text-sm text-gray-500">No donors found matching your criteria. Please try a different search or check back later.</p>
                </div>

            ) : (
                <div className="space-y-4">
                    {results.map(donor => (
                        <div key={donor.id} className="bg-white p-4 sm:p-6 rounded-lg shadow-lg border border-red-100 hover:shadow-xl transition-shadow duration-300 ease-in-out">
                            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                                <div className="mb-3 sm:mb-0">
                                    <h3 className="text-xl font-semibold text-red-600">{donor.name}</h3>
                                    <p className="text-sm text-gray-500">City: {donor.city}</p>
                                </div>
                                <div className="text-left sm:text-right">
                                     <p className="text-sm text-gray-700">Blood Type: <span className="font-bold text-lg text-red-700">{donor.bloodType}</span></p>
                                     <p className="text-xs text-gray-500">Last Donated: {donor.lastDonationDate?.seconds ? new Date(donor.lastDonationDate.seconds * 1000).toLocaleDateString() : 'Not specified'}</p>
                                </div>
                            </div>
                           
                            {donor.wantsNotifications ? (
                                <button 
                                    onClick={() => handleNotifyClick(donor)}
                                    className="mt-4 w-full sm:w-auto px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors text-sm shadow hover:shadow-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
                                >
                                    Show Contact Info / Notify (Simulated)
                                </button>
                            ) : (
                                <p className="mt-4 text-sm text-gray-500 italic bg-gray-50 p-2 rounded-md">Donor has not consented to direct contact.</p>
                            )}
                        </div>
                    ))}
                </div>
            )}

            {selectedDonor && (
                <Modal onClose={() => setSelectedDonor(null)}>
                    <h3 className="text-xl font-semibold text-red-700 mb-3">Contact Donor: {selectedDonor.name}</h3>
                    <p className="text-sm text-gray-600 mb-1">
                        This donor (<span className="font-medium">{selectedDonor.bloodType}</span> in <span className="font-medium">{selectedDonor.city}</span>) has agreed to be contacted.
                    </p>
                    <p className="text-sm text-gray-600 mb-3">
                        Please be respectful and clear about your needs.
                    </p>
                    <div className="bg-red-50 p-3 rounded-md border border-red-200 space-y-1">
                        <p><strong>Email:</strong> <a href={`mailto:${selectedDonor.email}`} className="text-blue-600 hover:underline">{selectedDonor.email}</a></p>
                        <p><strong>Phone:</strong> <a href={`tel:${selectedDonor.phone}`} className="text-blue-600 hover:underline">{selectedDonor.phone}</a></p>
                    </div>
                     <p className="text-xs text-gray-500 mt-4">
                        Note: This is a simulation. In a real application, an email/SMS might be sent, or you would contact them directly using the details above.
                    </p>
                </Modal>
            )}
            <button 
                onClick={() => setCurrentPage('search')} 
                className="mt-8 block mx-auto px-6 py-2.5 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-colors shadow hover:shadow-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
            >
                New Search
            </button>
        </div>
    );
}

export default ResultsModule;
