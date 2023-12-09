import {getStorage} from 'firebase/storage';
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyB_5lEACrfJvBiLiThJhPTOXFYp4dWq8Tc",
  authDomain: "numplate-face.firebaseapp.com",
  projectId: "numplate-face",
  storageBucket: "numplate-face.appspot.com",
  messagingSenderId: "748058112478",
  appId: "1:748058112478:web:f6f73fe751a67ba7a0ad4f"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const img_viddb=getStorage(app)