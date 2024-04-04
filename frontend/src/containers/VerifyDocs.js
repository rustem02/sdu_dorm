import React, { useContext, useEffect,useState } from 'react'
import axios from 'axios'
import AuthContext from '../context/AuthContext';
import { Link } from 'react-router-dom';


export default function VerifyDocs() {
    const {authTokens} = useContext(AuthContext)
    const [documents, setDocuments] = useState([]);
    const [verified,setVerified] = useState("")

    useEffect(()=>{
        const fetchDocuments = async() =>{
            try{
                const response = axios.get('documents/',{
                    headers: {
                        Authorization: `Bearer ${authTokens.access}` // Добавляем токен для аутентификации запроса
                      }
                })

                const res = (await response).data;
                setDocuments(res);

                // Создаем массив только с верифицированными пользователями
                const verifiedUsers = res.filter(doc => doc.is_verified).map(doc => doc.user_data.email);

                setVerified(verifiedUsers); // Сохраняем массив верифицированных пользователей
                console.log(verified);
            }catch(err){
                console.error('Ошибка при получении списка документов:', err);
            }
        }
        fetchDocuments()
    },[authTokens]);

    // В другом месте вашего компонента (или в другом useEffect)
    useEffect(() => {
        if (verified.length > 0) {
            console.log('Верифицированные пользователи:', verified);
        }
    }, [verified]);
    
    return (
    <div className='documents-list'>
        {documents.map((doc,index) => (
          <div key={index} className='documents-item' style={{backgroundColor: verified.includes(doc.user_data.email) ? 'lightgreen' : '#e1e1e1' }}>
            {doc.user_data.email}
            <Link 
            to = {{ pathname: `/detailed-doc/${doc.user_data.email}` }}>
                <a>detailed &gt;</a>
            </Link>
          </div> // Пример отображения документов
        ))}
    </div>
  )
}
