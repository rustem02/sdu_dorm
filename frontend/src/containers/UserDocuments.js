import axios from 'axios';
import React, { useContext, useEffect, useState } from 'react'
import { useLocation, useParams } from 'react-router-dom'
import AuthContext from '../context/AuthContext';


export default function UserDocuments() {
    const { email } = useParams();
    const {authTokens } = useContext(AuthContext)
    const [userDocuments, setUserDocuments] = useState([]);

    useEffect(()=>{
            const fetchDocuments = async() =>{
                try{
                    const response = axios.get(`user-documents/?email=${email}`,{
                        headers:{
                            'Authorization': `Bearer ${authTokens.access}`,
                        }
                    })
    
                    const res = (await response).data;
                    setUserDocuments(res);
                    console.log(res);
    
                }catch(err){
                    console.error('Ошибка при получении документов пользователя:', err);
                }
            }
            if(email){
                fetchDocuments()
            }
    },[email]);
    
    // useEffect(() => {
    //     if (userDocuments.length > 0) {
    //         console.log('Документы пользователя:', userDocuments);
    //     }
    // }, [userDocuments]);

    return (
    <div>
        <h2>Документы пользователя: {email}</h2>
        <div className='user-documents'>
            <div className='user-docs-item'>
                <p>Form 075</p>
                <img src={userDocuments.form_075} alt="dorm"/>
            </div>
            <div className='user-docs-item'>
                <p>Identity Card Copy</p>
                <img src={userDocuments.identity_card_copy} alt="dorm"/>
            </div>
            <div className='user-docs-item'>
                <p>Photo 3x4</p>
                <img src={userDocuments.photo_3x4} alt="dorm"/>
            </div>
            <div className='user-docs-item'>
                <p>Statement</p>
                <img src={userDocuments.statement} alt="dorm"/>
            </div>
        </div>
    </div>
  )
}

