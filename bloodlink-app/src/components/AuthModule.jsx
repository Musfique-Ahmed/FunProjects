// src/components/AuthModule.jsx
import React, { useState } from 'react';
// Import the initialized auth instance from your firebaseConfig.js
import { auth } from '../firebaseConfig'; // Assuming firebaseConfig.js is in src/
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword
} from 'firebase/auth';

function AuthModule({ setCurrentPage, setError, setLoading, setSuccessMessage, bloodGroups /* bloodGroups prop received but not used in this specific module, can be removed if not needed here */ }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isRegistering, setIsRegistering] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccessMessage('');
        try {
            if (isRegistering) {
                await createUserWithEmailAndPassword(auth, email, password);
                setSuccessMessage('Registration successful! Redirecting to dashboard...');
                // onAuthStateChanged in App.jsx will handle navigation
            } else {
                await signInWithEmailAndPassword(auth, email, password);
                setSuccessMessage('Login successful! Redirecting to dashboard...');
                // onAuthStateChanged in App.jsx will handle navigation
            }
        } catch (err) {
            console.error("Auth Error:", err);
            setError(err.message || "Authentication failed. Please check your credentials.");
        }
        setLoading(false);
    };

    return (
        <div className="max-w-md mx-auto bg-white p-6 sm:p-8 rounded-xl shadow-2xl">
            <h2 className="text-2xl sm:text-3xl font-bold text-center text-red-700 mb-6">
                {isRegistering ? 'Register as a Donor' : 'Donor Login'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Email</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
                        placeholder="you@example.com"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        minLength="6"
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm"
                        placeholder="••••••••"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
                >
                    {isRegistering ? 'Register' : 'Login'}
                </button>
            </form>
            <button
                onClick={() => setIsRegistering(!isRegistering)}
                className="mt-4 text-center w-full text-sm text-red-600 hover:text-red-800 hover:underline"
            >
                {isRegistering ? 'Already have an account? Login' : "Don't have an account? Register Now"}
            </button>
        </div>
    );
}

export default AuthModule;
