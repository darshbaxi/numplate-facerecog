import React, { useState } from 'react';
import { ref, uploadBytes } from 'firebase/storage';
import { v4 } from 'uuid';
import { img_viddb } from '../config';

export default function Registration() {
  const [user, setUser] = useState({
    upld: '',
    name: '',
    licence: '',
  });

  const [selected, setSelect] = useState(null);

  const getuserData = (e) => {
    const { name, value } = e.target;
    setUser({ ...user, [name]: value });
  };

  const postdata = async (e) => {
    e.preventDefault();
    const { upld, name, licence } = user;

    if (name && licence) {
      const res = await fetch('https://numplate-face-default-rtdb.firebaseio.com/num-face.json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, licence }),
      });

      if (res) {
        setUser({
          upld: '',
          name: '',
          licence: '',
        });
        window.location.reload();
      }
    } else {
      alert('Please fill the form');
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!selected) {
      alert('Please select a file');
      return;
    }

    const img_reg = ref(img_viddb, `Registration/${v4()}`);
    try {

      const ress=await uploadBytes(img_reg, selected);
      if(ress){
      alert("photo uploded successfully")
      setSelect(null);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <form className="Registration" onSubmit={postdata}>
        <div className="header">
          <h1>Registration</h1>
        </div>
        <div className="register">
          <input
            type="file"
            name="upld"
            onChange={(e) => setSelect(e.target.files[0])}
            className="upload"
            required
          />
          <button type="button" onClick={handleUpload}>
            Upload
          </button>
          <br />
          <input
            type="text"
            name="name"
            onChange={getuserData}
            value={user.name}
            placeholder="Enter your Name"
            className="name"
            required
          />
          <br />
          <input
            type="text"
            name="licence"
            onChange={getuserData}
            value={user.licence}
            placeholder="Enter your Vehicle Licence Number"
            className="licence"
            required
          />
        </div>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}