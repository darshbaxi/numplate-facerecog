import React, { useState } from 'react';
import { ref, uploadBytes } from 'firebase/storage';
import { v4 } from 'uuid';
import { img_viddb } from '../config';

function generateRandomString(length) {
  const uuidString = v4().replace(/-/g, ''); // Remove hyphens from the UUID
  return uuidString.slice(0, length);
}

const IDPers = generateRandomString(10);

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

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selected || !user.name || !user.licence) {
      alert('Please fill out all the fields and upload a file');
      return;
    }

    try {
      // Upload image
      const img_reg = ref(img_viddb, `Registration/${IDPers}`);
      await uploadBytes(img_reg, selected);

      // Save data
      const res = await fetch(`https://numplate-face-default-rtdb.firebaseio.com/num-face/${IDPers}.json`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: user.name, licence: user.licence }),
      });

      if (res) {
        setUser({
          upld: '',
          name: '',
          licence: '',
        });
        setSelect(null);
        alert('Data submitted successfully');
        window.location.reload();
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <form className="Registration" onSubmit={handleSubmit}>
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
            placeholder="Enter your Vehicle License Number"
            className="license"
            required
          />
        </div>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}
