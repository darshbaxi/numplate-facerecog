import React,{ useState } from 'react'
import  {ref, uploadBytes} from "firebase/storage"; 
import {v4} from "uuid";
import { img_viddb } from '../config';

function Home() {


    const [selectedFile, setSelectedFile] = useState(null);
        
    
    const handleUpload = async (e) => {
      e.preventDefault();
      const img_vidref = ref(img_viddb, `files/${v4()}`);
      console.log(selectedFile);
    
      try {
        const res = await uploadBytes(img_vidref, selectedFile);
        if (res) {
          window.location.reload();
          setSelectedFile(null); 
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        
      }
    };
    
    
    
    
  
        return (
    <form className='validate'>
      <div className='header'>
        <h1>Upload the video/photo for validation</h1>
      </div>
      <div className='upload'>
        <input type='file' onChange={(e)=>setSelectedFile(e.target.files[0])}/>
        <button onClick={handleUpload}>Upload Video</button>
      </div>
    </form>
  )
}
export default Home;