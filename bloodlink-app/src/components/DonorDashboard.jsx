// src/components/DonorDashboard.jsx
import React, { useState, useEffect } from 'react';
// Import db, appId, and Timestamp from your firebaseConfig.js and firebase/firestore
import { db, appId } from '../firebaseConfig'; // Assuming firebaseConfig.js is in src/
import { doc, setDoc, Timestamp } from 'firebase/firestore';

function DonorDashboard({
    user,
    donorDetails,
    setDonorDetails,
    setError,
    setLoading,
    setSuccessMessage,
    showDonorForm,
    setShowDonorForm,
    generateThankYouMessage,
    bloodGroups // Prop received from App.jsx
}) {
    const initialFormData = {
        name: '',
        phone: '',
        bloodType: bloodGroups[0], // Default to the first blood group
        city: '',
        lastDonationDate: '',
        wantsNotifications: true,
    };

    const [formData, setFormData] = useState(initialFormData);
    const [isEditing, setIsEditing] = useState(showDonorForm || !donorDetails);

    useEffect(() => {
        if (donorDetails) {
            setFormData({
                name: donorDetails.name || user?.displayName || '',
                phone: donorDetails.phone || '',
                bloodType: donorDetails.bloodType || bloodGroups[0],
                city: donorDetails.city || '',
                lastDonationDate: donorDetails.lastDonationDate?.seconds 
                    ? new Date(donorDetails.lastDonationDate.seconds * 1000).toISOString().split('T')[0] 
                    : '',
                wantsNotifications: donorDetails.wantsNotifications !== undefined ? donorDetails.wantsNotifications : true,
            });
            setIsEditing(showDonorForm); // Respect showDonorForm prop
        } else if (user) {
            // If no donor details, prefill with user's display name if available, and set to editing
            setFormData(prev => ({
                ...initialFormData, // Start with defaults
                name: user.displayName || '',
                // email is not part of this form but available in 'user' object
            }));
            setIsEditing(true);
        }
    }, [donorDetails, user, showDonorForm, bloodGroups]);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccessMessage('');

        if (!formData.name || !formData.bloodType || !formData.city || !formData.phone) {
            setError("Name, Phone, Blood Type, and City are required.");
            setLoading(false);
            return;
        }
        
        const donorDataToSave = {
            ...formData,
            userId: user.uid,
            email: user.email, 
            updatedAt: Timestamp.now(),
            lastDonationDate: formData.lastDonationDate ? Timestamp.fromDate(new Date(formData.lastDonationDate)) : null,
        };

        try {
            const donorRef = doc(db, `/artifacts/${appId}/public/data/donors`, user.uid);
            await setDoc(donorRef, donorDataToSave, { merge: true });
            setDonorDetails(donorDataToSave); 
            
            const thankYouMsg = await generateThankYouMessage(donorDataToSave.name, donorDataToSave.bloodType, donorDataToSave.city);
            setSuccessMessage(thankYouMsg || 'Profile updated successfully!');
            
            setIsEditing(false);
            setShowDonorForm(false); 
        } catch (err) {
            console.error("Error saving donor details:", err);
            setError('Failed to save profile: ' + (err.message || "Unknown error occurred."));
        }
        setLoading(false);
    };
    
    if (!user || user.isAnonymous) { // Ensure user is logged in and not anonymous
        return <p className="text-center text-red-700">Please log in to manage your donor profile.</p>;
    }

    return (
        <div className="max-w-lg mx-auto bg-white p-6 sm:p-8 rounded-xl shadow-2xl">
            <h2 className="text-2xl sm:text-3xl font-bold text-center text-red-700 mb-6">My Donor Profile</h2>
            {isEditing ? (
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Full Name</label>
                        <input type="text" name="name" value={formData.name} onChange={handleChange} required
                               className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Phone Number</label>
                        <input type="tel" name="phone" value={formData.phone} onChange={handleChange} required
                               className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500" placeholder="e.g., +1234567890" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Blood Type</label>
                        <select name="bloodType" value={formData.bloodType} onChange={handleChange} required
                                className="mt-1 block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500">
                            {bloodGroups.map(bg => <option key={bg} value={bg}>{bg}</option>)}
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">City</label>
                        <input type="text" name="city" value={formData.city} onChange={handleChange} required
                               className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500" placeholder="Your City" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Last Donation Date (Optional)</label>
                        <input type="date" name="lastDonationDate" value={formData.lastDonationDate} onChange={handleChange}
                               className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500" />
                    </div>
                    <div className="flex items-center">
                        <input type="checkbox" name="wantsNotifications" id="wantsNotifications" checked={formData.wantsNotifications} onChange={handleChange}
                               className="h-4 w-4 text-red-600 border-gray-300 rounded focus:ring-red-500" />
                        <label htmlFor="wantsNotifications" className="ml-2 block text-sm text-gray-900">
                            I agree to be contacted by email/phone if I am a potential match.
                        </label>
                    </div>
                    <div className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-3">
                        <button type="submit"
                                className="flex-1 w-full justify-center py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors">
                            Save Profile
                        </button>
                        {donorDetails &&  // Show cancel only if there were details before editing
                            <button type="button" onClick={() => { setIsEditing(false); setShowDonorForm(false); setFormData(donorDetails); /* Reset form to original details */}}
                                className="flex-1 w-full justify-center py-2.5 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors">
                                Cancel
                            </button>
                        }
                    </div>
                </form>
            ) : donorDetails ? (
                <div className="space-y-3 text-gray-700">
                    <p><strong>Name:</strong> {donorDetails.name}</p>
                    <p><strong>Email:</strong> {donorDetails.email}</p>
                    <p><strong>Phone:</strong> {donorDetails.phone}</p>
                    <p><strong>Blood Type:</strong> <span className="font-semibold text-red-600">{donorDetails.bloodType}</span></p>
                    <p><strong>City:</strong> {donorDetails.city}</p>
                    <p><strong>Last Donated:</strong> {donorDetails.lastDonationDate?.seconds ? new Date(donorDetails.lastDonationDate.seconds * 1000).toLocaleDateString() : 'Not specified'}</p>
                    <p><strong>Contact Consent:</strong> {donorDetails.wantsNotifications ? <span className="text-green-600 font-medium">Yes</span> : <span className="text-red-600 font-medium">No</span>}</p>
                    <button onClick={() => {setIsEditing(true); setShowDonorForm(true);}}
                            className="mt-4 w-full flex justify-center py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors">
                        Edit Profile
                    </button>
                </div>
            ) : (
                 <div className="text-center">
                    <p className="mb-4 text-gray-600">You haven't registered your donor details yet.</p>
                    <button onClick={() => {setIsEditing(true); setShowDonorForm(true);}}
                            className="mt-4 w-full flex justify-center py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors">
                        Register as a Donor Now
                    </button>
                </div>
            )}
        </div>
    );
}

export default DonorDashboard;
