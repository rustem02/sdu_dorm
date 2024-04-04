import React from 'react'
import { Link, Navigate } from 'react-router-dom'
import { useState } from 'react'
import axios from 'axios'

export default function Register() {
  const [first_name, setName] = useState('')
  const [last_name, setLastName] = useState('')
  const [id_number, setIdNum] = useState('')
  const [specialty, setSpecialty] = useState('')
  const [faculty, setFaculty] = useState('')
  const [birth_date, setBirthDate] = useState('')
  const [gender, setGender] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [password_confirm, setConfirmPassword] = useState('')
  const [redirect, setRedirect] = useState(false)

  const submit = async (e) =>{
    e.preventDefault();
    
     await axios.post('register/', {
        first_name, last_name, id_number, specialty, faculty, birth_date, gender, email, password, password_confirm
    });

    // const content = await response.json();

    setRedirect(true);
  }

  if(redirect){
      return <Navigate to='/' replace />;
  }

  return (
    <main>
      <div className="welcome">
          <div className="welcome-items">
              <div className="img">
                  <img src={require('../img/SignUpImg.png')} alt="img"/>
              </div>
              <div className="welcome-content">
                  <h2 className="welcome-title">Welcome to Dorm Hub platform!</h2>
                  <p className="welcome-desc">Welcome to Dorm Hub platform ! Dorm Hub is an online platform developed in the user friendly interface to make it easier for SDU students to book a seat in a dormitory.</p>
              </div>
          </div>
      </div>
      <div className="signing">
          <div className="container container-up">
              <div className="form-content">
                  <div className="title-content title-content-up">
                      <h2>Sign up</h2>
                      <p>To sign up in the system, please fill out the forms below.</p>
                  </div>
                  <form onSubmit={submit}>
                    <div className="field-component field-signup">
                      <input 
                      type="text" placeholder="First Name" id="first_name"
                      onChange={e => setName(e.target.value)}
                      required
                      />
                    </div>
                    <div className="field-component field-signup">
                      <input 
                      type="text" placeholder="Last Name" id="last_name"
                      onChange={e => setLastName(e.target.value)}
                      required
                      />
                    </div>
                    <div className="field-component field-signup">
                      <input 
                      type="email" placeholder="Email" id="email"
                      onChange={e => setEmail(e.target.value)}
                      required
                      />
                    </div>
                    <div className="field-component field-signup">
                      <input 
                      type="number" placeholder="ID number" id="id_number"
                      onChange={e => setIdNum(e.target.value)}
                      required
                      />
                      
                    </div>
                    <div className="field-component field-signup">
                      <input 
                      type="number" placeholder="Specialty number" id="specialty"
                      onChange={e => setSpecialty(e.target.value)}
                      required
                      />
                      
                    </div>
                    <div className="field-component field-signup">
                      <input 
                      type="number" placeholder="Faculty" id="faculty"
                      onChange={e => setFaculty(e.target.value)}
                      required
                      />
                    </div>
                    <div className="field-component field-signup">
                      <input 
                      type="date" placeholder="Birth date" id="birth_date"
                      onChange={e => setBirthDate(e.target.value)}
                      required
                      />
                    </div>
                    <div className="field-component field-signup">
                      <input 
                      type="text" placeholder="Gender" id="gender"
                      onChange={e => setGender(e.target.value)}
                      required
                      />
                    </div>
                    <div className="field-component field-signup">
                      <input 
                      type="password" placeholder="Create Password" id="password"
                      onChange={e => setPassword(e.target.value)}
                      required
                      />
                    </div>
                    <div className="field-component field-signup">
                      <input 
                      type="password" placeholder="Confirm Password" id="password_confirm"
                      onChange={e => setConfirmPassword(e.target.value)}
                      required
                      />
                    </div>
                    <div class="additional">
                        <div class="remember-chkbx">
                            <input type="checkbox" name="remember" id="remember"/>
                            <label for="remember">I agree to the privacy terms</label>
                        </div>
                    </div>
                    <button className="btn">Sign up</button>
                  </form>
              </div>
              <h4>Do you already have an account? <Link to = '/'>Click here</Link></h4>
          </div>
      </div>
</main>
  )
}
