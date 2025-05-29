// src/firebaseConfig.js
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

// =====================================================================================
// IMPORTANT: REPLACE THE PLACEHOLDER VALUES BELOW WITH YOUR ACTUAL FIREBASE PROJECT'S
// CONFIGURATION! YOU CAN GET THIS FROM THE FIREBASE CONSOLE:
// Project settings > General > Your apps > Web app > Firebase SDK snippet > Config
// =====================================================================================
const firebaseConfig = {
  apiKey: "AIzaSyBwLExSclRjYOVcUGsoqX7evGGtcs7P6Ok",
  authDomain: "bloodlink-connect-3f628.firebaseapp.com",
  projectId: "bloodlink-connect-3f628",
  storageBucket: "bloodlink-connect-3f628.firebasestorage.app",
  messagingSenderId: "916093332332",
  appId: "1:916093332332:web:b48bc219215c030a4da149",
  measurementId: "G-8RNQS3GH05"                             // Replace with your actual app ID
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// You might need a consistent appId string for your Firestore paths,
// especially if you were using the {appId} variable from the Canvas environment in paths.
// If your Firestore paths were like `/artifacts/${appId}/...`, ensure this 'appId' constant
// matches what you intend to use or matches your security rules.
// For simplicity, you can often just use your projectId or a unique app name if needed in paths,
// or adapt your Firestore paths in the components to not require this specific structure.
// For now, let's export the one from the config, but be mindful of its use in paths.
const appIdString = firebaseConfig.appId;

export { auth, db, appIdString as appId }; // Exporting appIdString as appId for consistency if Canvas code used 'appId'