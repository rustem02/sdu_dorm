import React  from 'react'
import Navbar from '../components/Navbar'
import { Link } from 'react-router-dom'

export default function MainPage() {

  return (
    <>
        <Navbar/>
        <section className="wrapper header">
            <header>
                <div className="title-main">
                    <h1>Booking platform —Dorm Hub</h1>
                    <p>This website is intended for booking places in the "SDU University" dormitories. It’s a user friendly platform that will allow all students, especially first-year students who want to live in dormitories, to book places while at home. Because this platform allows students to adapt easily and book with peace of mind. </p>
                    <div className="btn-group">
                        <button className="btn-book">Book Now</button>
                        <Link to="/document-submission"><button className="btn-submission">Document Submission</button></Link>
                    </div>
                </div>
                <div className="dorm-img">
                    <img src={require('../img/dorm-img.png')} alt="dorm"/>
                </div>
            </header>
        </section>
        <section className="main-points">
            <h2></h2>
            <div class="vision">
                
            </div>
            <button className="learn-more"></button>
        </section>
  </>

  )
}
