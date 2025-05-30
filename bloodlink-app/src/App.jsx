// src/App.jsx
import React, { useState, useEffect } from 'react';
import { auth, db, appId } from './firebaseConfig'; // Ensure this path is correct and file is configured
import {
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    signOut,
    onAuthStateChanged,
    signInAnonymously,
    signInWithCustomToken
} from 'firebase/auth';
import {
    doc,
    setDoc,
    getDoc,
    collection,
    query,
    where,
    getDocs,
    Timestamp
} from 'firebase/firestore';

// Import child components from the src/components/ folder
import AuthModule from './components/AuthModule';
import DonorDashboard from './components/DonorDashboard';
import SearchModule from './components/SearchModule';
import ResultsModule from './components/ResultsModule';

const bloodGroups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];

function App() {
    const [user, setUser] = useState(null);
    const [userId, setUserId] = useState(null);
    const [isAuthReady, setIsAuthReady] = useState(false);
    const [currentPage, setCurrentPage] = useState('search');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const [donorDetails, setDonorDetails] = useState(null);
    const [showDonorForm, setShowDonorForm] = useState(false);

    const [searchResults, setSearchResults] = useState([]);
    const [searchCriteria, setSearchCriteria] = useState(null);

    const clearMessages = () => {
        setError('');
        setSuccessMessage('');
    };
    
    const navigate = (page) => {
        clearMessages();
        setCurrentPage(page);
        // Logic to show donor form if user is logged in, on dashboard, but has no details
        if (page === 'donorDashboard' && user && !user.isAnonymous && !donorDetails) {
            setShowDonorForm(true); 
        } else if (page === 'donorDashboard' && donorDetails) {
            setShowDonorForm(false); 
        }
    };

    useEffect(() => {
        setLoading(true); 
        const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
            if (currentUser) {
                setUser(currentUser);
                setUserId(currentUser.uid);
                if (!currentUser.isAnonymous) {
                    const donorRef = doc(db, `/artifacts/${appId}/public/data/donors`, currentUser.uid);
                    try {
                        const donorSnap = await getDoc(donorRef);
                        if (donorSnap.exists()) {
                            setDonorDetails(donorSnap.data());
                        } else {
                            setDonorDetails(null); 
                        }
                        // If user just logged in/registered (was on auth page) or is already on dashboard, stay/go to dashboard
                        if (currentPage === 'auth' || currentPage === 'donorDashboard') {
                           setCurrentPage('donorDashboard');
                           if (!donorSnap.exists()) {
                               setShowDonorForm(true); // Prompt to create profile if it doesn't exist
                           } else {
                               setShowDonorForm(false);
                           }
                        }
                    } catch (dbError) {
                        console.error("Error fetching donor details:", dbError);
                        setError("Could not fetch your profile data. Please try again later.");
                        if (currentPage === 'auth' || currentPage === 'donorDashboard') {
                           setCurrentPage('donorDashboard'); // Still go to dashboard but show error
                        }
                    }
                } else { // User is anonymous
                    setDonorDetails(null); // Anonymous users don't have donor profiles
                    if (currentPage !== 'search' && currentPage !== 'results') {
                        setCurrentPage('search'); // Default anonymous users to search page
                    }
                }
            } else { // No user (logged out)
                setUser(null);
                setUserId(null);
                setDonorDetails(null);
                // Attempt anonymous sign-in for guest functionality
                try {
                    // Check if an anonymous session already exists to prevent multiple sign-ins if not necessary
                    if (!auth.currentUser) { 
                       await signInAnonymously(auth);
                    }
                    // onAuthStateChanged will run again with the new anonymous user
                } catch (anonError) {
                    console.error("Automatic anonymous sign-in failed after logout/initial load:", anonError);
                    setError("Could not initialize guest session. Please refresh the page.");
                }
                // If user was on a page requiring login, redirect to search or auth
                if (currentPage === 'donorDashboard') {
                    setCurrentPage('auth');
                } else if (currentPage !== 'search' && currentPage !== 'results' && currentPage !== 'auth') {
                    setCurrentPage('search');
                }
            }
            setIsAuthReady(true);
            setLoading(false); 
        });
        
        // Optional: Attempt custom token sign-in if __initial_auth_token is defined
        // This is usually for specific environments like Canvas, not standard local dev.
        const attemptCustomTokenSignIn = async () => {
            const localInitialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;
            if (localInitialAuthToken && !auth.currentUser) { // Only if token exists and no user is signed in
                setLoading(true);
                try {
                    await signInWithCustomToken(auth, localInitialAuthToken);
                    // onAuthStateChanged will handle the rest
                } catch (e) {
                    console.error("Custom token sign-in error:", e);
                    setError("Authentication failed. Trying guest session.");
                    if (!auth.currentUser) await signInAnonymously(auth).catch(err => console.error("Fallback anon sign-in failed", err));
                } finally {
                    setLoading(false);
                }
            }
        };
        attemptCustomTokenSignIn();

        return () => unsubscribe();
    }, [appId, currentPage]); // Added currentPage to dependencies

    const handleLogout = async () => {
        setLoading(true);
        try {
            const wasAnonymous = user?.isAnonymous;
            await signOut(auth);
            // onAuthStateChanged will handle setting user to null and then re-triggering anonymous sign-in
            setSuccessMessage('Logged out successfully.');
            // No need to explicitly call signInAnonymously here, onAuthStateChanged handles it.
            // setCurrentPage('search'); // Let onAuthStateChanged redirect appropriately
        } catch (e) {
            console.error('Logout failed:', e);
            setError('Logout failed: ' + e.message);
        }
        setLoading(false);
    };

    const generateThankYouMessage = async (name, bloodType, city) => {
        const prompt = `Generate a short, encouraging, and thankful message for a blood donor named ${name} who has just registered their details with blood type ${bloodType} in ${city}. Mention the importance of their contribution. Keep it under 30 words.`;
        let chatHistory = [{ role: "user", parts: [{ text: prompt }] }];
        const payload = { contents: chatHistory };
        const apiKey = ""; // For gemini-2.0-flash, API key might be handled by the environment
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

        try {
            setLoading(true);
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ message: "Unknown LLM API error" }));
                console.error("LLM API Error Response:", errorData);
                throw new Error(`LLM API request failed. ${errorData.error?.message || errorData.message || ''}`);
            }
            const result = await response.json();
            setLoading(false);
            if (result.candidates && result.candidates[0]?.content?.parts[0]?.text) {
                return result.candidates[0].content.parts[0].text;
            }
            return "Thank you for your valuable contribution!"; // Fallback
        } catch (error) {
            setLoading(false);
            console.error("Error generating thank you message:", error);
            return `Thank you, ${name}! Your registration as a donor of ${bloodType} blood in ${city} is highly appreciated.`; // Enhanced fallback
        }
    };

    if (!isAuthReady) {
        return <LoadingSpinner />;
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-red-100 via-red-50 to-pink-100 font-sans flex flex-col">
            <header className="bg-red-600 text-white p-4 shadow-lg sticky top-0 z-10">
                <div className="container mx-auto flex flex-wrap items-center justify-between">
                    <h1 className="text-2xl sm:text-3xl font-bold cursor-pointer" onClick={() => navigate(user && !user.isAnonymous ? 'donorDashboard' : 'search')}>
                        BloodLink Connect
                    </h1>
                    <nav className="flex flex-wrap items-center space-x-2 sm:space-x-4 text-sm sm:text-base">
                        {user && !user.isAnonymous && <span className="hidden sm:inline">Welcome, {user.displayName || user.email || 'Donor'}!</span>}
                        {userId && <span className="text-xs px-2 py-1 bg-red-700 rounded">User ID: {userId.substring(0,8)}...</span>}
                        <button onClick={() => navigate('search')} className="hover:bg-red-700 px-3 py-2 rounded-md transition-colors">Find Blood</button>
                        {user && !user.isAnonymous ? (
                            <>
                                <button onClick={() => navigate('donorDashboard')} className="hover:bg-red-700 px-3 py-2 rounded-md transition-colors">My Dashboard</button>
                                <button onClick={handleLogout} className="bg-red-500 hover:bg-red-700 px-3 py-2 rounded-md transition-colors">Logout</button>
                            </>
                        ) : (
                            <button onClick={() => navigate('auth')} className="bg-red-500 hover:bg-red-700 px-3 py-2 rounded-md transition-colors">Register/Login</button>
                        )}
                    </nav>
                </div>
            </header>

            <main className="w-full p-4 sm:p-6 mt-4 flex-grow">
                {error && <AlertMessage type="error" message={error} onClose={clearMessages} />}
                {successMessage && <AlertMessage type="success" message={successMessage} onClose={clearMessages} />}

                {currentPage === 'auth' && <AuthModule setCurrentPage={navigate} setError={setError} setLoading={setLoading} setSuccessMessage={setSuccessMessage} bloodGroups={bloodGroups} />}
                
                {currentPage === 'donorDashboard' && user && !user.isAnonymous && (
                    <DonorDashboard 
                        user={user} 
                        donorDetails={donorDetails} 
                        setDonorDetails={setDonorDetails} 
                        setError={setError} 
                        setLoading={setLoading}
                        setSuccessMessage={setSuccessMessage}
                        showDonorForm={showDonorForm}
                        setShowDonorForm={setShowDonorForm}
                        generateThankYouMessage={generateThankYouMessage}
                        bloodGroups={bloodGroups}
                    />
                )}
                 {currentPage === 'donorDashboard' && (!user || (user && user.isAnonymous)) && (
                    <div className="text-center p-6 bg-white rounded-xl shadow-xl">
                        <p className="text-red-700 text-lg">Please register or log in to access your donor dashboard.</p>
                        <button onClick={() => navigate('auth')} className="mt-4 px-6 py-2 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-colors shadow-md">
                            Go to Register/Login
                        </button>
                    </div>
                )}

                {currentPage === 'search' && (
                    <SearchModule 
                        setSearchResults={setSearchResults} 
                        setCurrentPage={navigate} 
                        setError={setError} 
                        setLoading={setLoading}
                        setSearchCriteria={setSearchCriteria}
                        bloodGroups={bloodGroups}
                        setSuccessMessage={setSuccessMessage}
                    />
                )}
                {currentPage === 'results' && (
                    <ResultsModule 
                        results={searchResults} 
                        searchCriteria={searchCriteria}
                        setCurrentPage={navigate} 
                        setError={setError}
                    />
                )}
            </main>

            <footer className="bg-gray-800 text-white text-center p-4 mt-auto">
                <p>&copy; {new Date().getFullYear()} BloodLink Connect. All rights reserved.</p>
                <p className="text-xs mt-1">This platform connects donors and recipients. Verify information independently.</p>
            </footer>
            {loading && <LoadingSpinner />}
        </div>
    );
}

// Utility Components
function LoadingSpinner() {
    return (
        <div className="fixed inset-0 bg-gray-700 bg-opacity-60 flex flex-col items-center justify-center z-50 backdrop-blur-sm">
            <div className="animate-spin rounded-full h-16 w-16 sm:h-20 sm:w-20 border-t-4 border-b-4 border-red-500"></div>
            <p className="mt-4 text-white text-lg font-semibold">Loading, please wait...</p>
        </div>
    );
}

function AlertMessage({ type, message, onClose }) {
    const baseClasses = "border-l-4 p-4 rounded-md shadow-lg mb-6";
    const typeClasses = type === 'error' 
        ? 'bg-red-100 border-red-600 text-red-800' 
        : 'bg-green-100 border-green-600 text-green-800';
    const IconSvg = type === 'error' ? (
        <svg className="w-6 h-6 text-red-600 mr-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
    ) : (
        <svg className="w-6 h-6 text-green-600 mr-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
    );

    return (
        <div className={`${baseClasses} ${typeClasses}`} role="alert">
            <div className="flex items-start">
                {IconSvg}
                <div className="flex-grow">
                    <p className="font-bold text-lg">{type === 'error' ? 'Error Occurred' : 'Success!'}</p>
                    <p className="text-sm break-words">{message}</p>
                </div>
                <button onClick={onClose} className="ml-3 -mx-1.5 -my-1.5 bg-transparent rounded-lg focus:ring-2 p-1.5 inline-flex h-8 w-8 shrink-0" 
                        aria-label="Dismiss"
                        style={type === 'error' ? {color: 'rgb(185 28 28)', focusRingColor: 'rgb(220 38 38 / 0.5)'} : {color: 'rgb(22 101 52)', focusRingColor: 'rgb(34 197 94 / 0.5)'}}>
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd"></path></svg>
                </button>
            </div>
        </div>
    );
}

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

export default App;
