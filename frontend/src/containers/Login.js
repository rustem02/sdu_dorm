import axios from 'axios';
import React from 'react'
import {useState } from 'react'
import { Link, Navigate } from 'react-router-dom';
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';

const Login = ()=> {

  let {loginUser} = useContext(AuthContext)

  //Если пользователь авторизовался то кидать на MainPage
  return (
    <main>
        <div className='signing'>
            <div className='container'>
                <div className='logo'>
                    <img src={require('../img/logoDorm.png')} alt={'logo'} />
                </div>
                <div className="form-content">
                    <div className="title-content">
                        <h2>Sign in</h2>
                        <p>Welcome back, please sign in to your account.</p>
                    </div>
                    <form onSubmit={loginUser}>
                      <div className="field-component">
                        <label htmlFor="email">Email</label>
                        <input 
                        type="email" 
                        id="email"
                        name="email"
                        // autoComplete='off'
                        // onChange={e => setEmail(e.target.value)}
                        // value={email}
                        required
                        placeholder="Enter the email" 
                        />
                      </div>
                      <div className="field-component">
                        <label htmlFor="password">Password</label>
                        <input 
                        type="password" 
                        id="password"
                        // onChange={e => setPassword(e.target.value)}
                        // value={password}
                        required
                        placeholder="Enter the password" 
                        />
                      </div>
                      <div className="additional">
                         <div className="remember-chkbx">
                          <input 
                            type="checkbox" 
                            name="remember" 
                            id="remember" 
                          />
                         <label>Remember me</label>
                        </div>
                        <div className="forgot">
                          <a href="/"><Link to='/reset-password'>Forgot Password?</Link></a>
                        </div>
                      </div>
                      <button className="btn">Sign in</button>
                    </form>
                </div>
                <h4>If you don't have an account? <Link to ='/register'>Click here</Link></h4>
            </div>
        </div>
        <div className="welcome">
            <div className="welcome-items">
                <div className="img">
                    <img src={require('../img/SignInImg.png')} alt={"img"} />
                </div>
                <div className="welcome-content">
                    <h2 className="welcome-title">Welcome to Dorm Hub platform!</h2>
                    <p className="welcome-desc">Dorm Hub platform is an online platform developed in the user friendly interface to make it easier for SDU students to book a seat in a dormitory.</p>
                </div>
            </div>
        </div>
    </main>
    );
  };

// const mapStateToProps = state =>({
//   //Авторизовался?
// });

export default Login;
    // </>
  // )
// }
