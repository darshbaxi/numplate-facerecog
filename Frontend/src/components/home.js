import React,{ useState } from 'react'
import  {ref, uploadBytes} from "firebase/storage"; 
import {v4} from "uuid";
import { img_viddb } from '../config';
import axios from 'axios';


function generateRandomString(length) {
  const uuidString = v4().replace(/-/g, ''); // Remove hyphens from the UUID
  return uuidString.slice(0, length);
}

// Example: Generate a random string of length 10
const fileName = generateRandomString(10);


function Home() {


    const [selectedFile, setSelectedFile] = useState(null);
    const [responseArray, setResponseArray] = useState([]);
    
    const UpFileName = `Files/${fileName}`
    const handleUpload = async (e) => {
      e.preventDefault();
      const img_vidref = ref(img_viddb, UpFileName);
      console.log(selectedFile);
    
      try {
        const res = await uploadBytes(img_vidref, selectedFile);
        if (res) {
        
          setSelectedFile(null); 
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        
      }
      try {
        const response = await axios.post('http://localhost:8000/process_data', { data: UpFileName });
        // console.log("succ")
        // Log the response from the FastAPI backend
        console.log('Response from FastAPI:', response);
        setResponseArray(response.data); // Assuming the array is in the 'data' property of the response
      } catch (error) {
        console.error('Error in the FastAPI request:', error);
      }
  
    };
    
        return (
          <div>
          <form className='validate'>
            <div className='header'>
              <h1>Upload the video/photo for validation</h1>
            </div>
            <div className='upload'>
              <input type='file' onChange={(e) => setSelectedFile(e.target.files[0])} />
              <button onClick={handleUpload}>Upload Video</button>
            </div>
          </form>
    
          {/* Display the response array on the page */}
          <div className='response'>
            {responseArray.map((item, index) => (
              <div key={index}>{item}</div>
            ))}
          </div>
        </div>
      
  )
}
export default Home;