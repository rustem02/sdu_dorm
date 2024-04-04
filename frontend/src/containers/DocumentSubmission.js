import React from 'react'
import Navbar from '../components/Navbar'
import { useState } from 'react'
import axios from 'axios'
import AuthContext from '../context/AuthContext'
import { useContext } from 'react'

export default function DocumentSubmission() {
    const {authTokens} = useContext(AuthContext);

  const [statement, setStatement] = useState('')
  const [photo_3x4, setPhoto] = useState('')
  const [form_075, setForm] = useState('')
  const [identity_card_copy, setCardCopy] = useState('')
  const [redirect, setRedirect] = useState(false)
    
    const submit = async(e) =>{
        e.preventDefault();

        if(!statement || !photo_3x4 || !form_075 || !identity_card_copy){
            console.log("Files don't uploaded fully!");
        }else{
            const formData = new FormData()
            formData.append('statement', statement);
            formData.append('photo_3x4', photo_3x4);
            formData.append('form_075', form_075);
            formData.append('identity_card_copy', identity_card_copy);
            
            try{
                const response = axios.post('documents/upload/',formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': `Bearer ${authTokens.access}`,
                    },
                });

                // Обработка успешного ответа
                console.log(response.data);
                alert('Файлы успешно загружены');
            }catch(err){
                console.error('You have problems: ' + err)
            }
        }
    }

  return (
    <>
        <main className='submission'>
            <Navbar/>
            <div className='wrapper submission-content'>
                <div className='submission-list'>
                    <div>
                        <img src={require('../img/logoDorm.png')} alt="subm-logo"/> 
                        <h2>Required documents list</h2>
                        <p className='here'>Here, there is a list of required documents, carefully familiarize yourself with the list, upload them and send them for validation.</p>
                        <div className='list-doc'>
                            <ul>
                                <li>3x4 photo</li>
                                <li>075 form</li>
                                <li>identity card(copy)</li>
                                <li>letter of attorney</li>
                                <li>address certificate</li>
                                <li>university admission form</li>
                            </ul>
                        </div> 
                        <p>If you need an instructional video, click here</p> 
                    </div>
                </div>
                <div className='submission-material'>
                    <div>
                        <h2>Upload</h2>
                        <form onSubmit={submit}>
                            <input
                             type="file" id="statement" name="statement"
                             onChange={e => setStatement(e.target.files[0])}
                             required
                             />
                            <input 
                             type="file" id="photo_3x4" name="photo_3x4"
                             onChange={e => setPhoto(e.target.files[0])}
                             required
                            />
                            <input 
                             type="file" id="form_075" name="form_075"
                             onChange={e => setForm(e.target.files[0])}
                             required
                            />
                            <input 
                             type="file" id="identity_card_copy" name="identity_card_copy"
                             onChange={e => setCardCopy(e.target.files[0])}
                             required
                             />
                            <button>Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        </main>

    </>
  )
}
