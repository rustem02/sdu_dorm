import React, { useContext, useEffect,useState } from 'react'
import AuthContext from '../context/AuthContext';
import { Link } from 'react-router-dom';

export default function Navbar() {
  const { authTokens, logoutUser } = useContext(AuthContext);
  const [name, setName] = useState("");
  const [isStaff, setStaff] = useState("");

  let menu = document.getElementById('burger-menu')

  useEffect(() => {
    if (authTokens) {
      const userInfo = authTokens.user
      setName(userInfo.first_name);
      setStaff(userInfo.is_staff) // Предполагая, что email содержится в токене
    }
  }, [authTokens]);

  const changeBurgerMenu = ()=>{
       menu.classList.toggle('open-menu')
  }

  return (
    <nav className="nav">
        <div className="wrapper navbar-content">
          <div className="logo-nav">
              <img src={require('../img/logo-nav.png')} alt="logo"/>
          </div>
          <div className="navbar">
              <ul className="navbar-items">
                  <li><a href="">Home Page</a></li>
                  <li><a href="">Rooms</a></li>
                  <li><a href="">Booking</a></li>
                  <li><a href="">News</a></li>
                  <li><a href="">About Us</a></li>
                  <li className="nav-icons">
                      <button className="nav-btn">
                          <svg width="23" height="25" viewBox="0 0 23 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M11.5 25C13.2246 25 14.6236 23.6011 14.6236 21.875H8.3765C8.3765 23.6011 9.77542 25 11.5 25ZM22.0171 17.6899C21.0738 16.6763 19.3086 15.1514 19.3086 10.1562C19.3086 6.3623 16.6485 3.3252 13.0616 2.58008V1.5625C13.0616 0.699707 12.3623 0 11.5 0C10.6377 0 9.93851 0.699707 9.93851 1.5625V2.58008C6.3516 3.3252 3.69144 6.3623 3.69144 10.1562C3.69144 15.1514 1.9263 16.6763 0.982944 17.6899C0.689975 18.0049 0.560092 18.3813 0.562534 18.75C0.567905 19.5508 1.19632 20.3125 2.12992 20.3125H20.8702C21.8037 20.3125 22.4327 19.5508 22.4375 18.75C22.44 18.3813 22.3101 18.0044 22.0171 17.6899Z" fill="#F5F5F5" fill-opacity="0.6"/>
                          </svg>
                      </button>
                      <button className="nav-btn" onClick={changeBurgerMenu}>
                          <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M12.5 14.0625C16.3818 14.0625 19.5312 10.9131 19.5312 7.03125C19.5312 3.14941 16.3818 0 12.5 0C8.61816 0 5.46875 3.14941 5.46875 7.03125C5.46875 10.9131 8.61816 14.0625 12.5 14.0625ZM18.75 15.625H16.0596C14.9756 16.123 13.7695 16.4062 12.5 16.4062C11.2305 16.4062 10.0293 16.123 8.94043 15.625H6.25C2.79785 15.625 0 18.4229 0 21.875V22.6562C0 23.9502 1.0498 25 2.34375 25H22.6562C23.9502 25 25 23.9502 25 22.6562V21.875C25 18.4229 22.2021 15.625 18.75 15.625Z" fill="#F5F5F5" fill-opacity="0.6"/>
                          </svg>
                      </button>
                      <div id="burger-menu">
                        <div className="menu-item">
                            <p>{name}</p>
                        </div>
                        <div className="menu-item">
                            <p>My Profile</p>
                        </div>
                        <div className="menu-item">
                            <p>Booking History</p>
                        </div>
                        {isStaff && (
                            <div className="menu-item">
                                <Link to="/verify-documents"><p>Verify Documents</p></Link>
                            </div>
                        )}
                        <div className="menu-item">
                            <p>Support Chat</p>
                        </div>
                        <div className="menu-item" onClick={logoutUser}>
                            <p>Sign Out</p>
                        </div>
                    </div>                          
                  </li>
              </ul>
          </div>
      </div>
    </nav>
  )
}
