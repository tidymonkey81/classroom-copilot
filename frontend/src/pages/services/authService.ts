import { initializeApp } from 'firebase/app';
import { getAuth, signInWithEmailAndPassword, signOut } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyBPXoabdgnobFHYU4r3jv2nqY_qngmd70Q",
  authDomain: "classroom-copilot.firebaseapp.com",
  projectId: "classroom-copilot",
  storageBucket: "classroom-copilot.appspot.com",
  messagingSenderId: "449329145608",
  appId: "1:449329145608:web:5b97f804c62e408a492ebd"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth };

export const login = async (email: string, password: string) => {
  try {
    await signInWithEmailAndPassword(auth, email, password);
  } catch (error) {
    console.error("Login failed:", error);
    throw error;
  }
};

export const logout = async () => {
  try {
    await signOut(auth);
  } catch (error) {
    console.error("Logout failed:", error);
    throw error;
  }
};

export const getCurrentUser = () => {
  return auth.currentUser;
};