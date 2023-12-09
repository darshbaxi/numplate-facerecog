import React,{useState} from 'react'

export default function Registration () { 
   const [user,setuser]=useState({
    upld:"",
    name:"",
    licence:"",

   });
let nme,value;
   const getuserData=(e) =>{
    nme= e.target.name;
    value= e.target.value;

    setuser({...user,[nme]:value});
   };
   const postdata=async(e) =>{
      e.preventDefault();

      const {upld,name,licence} = user;
      
      if(upld && name && licence){
        const res=await fetch("https://numplate-face-default-rtdb.firebaseio.com/num-face.json",{
        method:"POST",
        headers:{
          "Content-Type":"application/json",
        },
        body:JSON.stringify( {upld,name,licence}),
      } );
      if(res){
        setuser({upld:"",
        name:"",
        licence:"",});
      }
   }
      else{
        alert("please fill the form")
      }

    }
  return (
    <div>
      <form className='Registration'>
      <div className='header'>
        <h1>Registration</h1>
      </div>
      <form className='regitration-form' method='POST'>
      <div className='register'>
        <input type='file' name='upld' onChange={getuserData} value={user.upld}  className='upload' required></input>
        <br></br>
        <input type='text' name='name' onChange={getuserData} value={user.name} placeholder='Enter your Name' className='name' required></input>
        <br></br>
        <input type='text' name='licence' onChange={getuserData} value={user.licence} placeholder='Enter your Vehicle Licence Number' className='lincence' required></input>
      </div>
      </form>
      <br></br>
      <button onClick={postdata}>submit</button>
    </form>
    </div>
  )

}