import axios from "axios";
import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import PrivateRoute from "./utils/PrivateRoute";

import MainPage from "./containers/MainPage";
import Login from "./containers/Login";
import Register from "./containers/Register";
import ResetPassword from "./containers/ResetPassword";
import DocumentSubmission from "./containers/DocumentSubmission";
import VerifyDocs from "./containers/VerifyDocs"; 
import UserDocuments from "./containers/UserDocuments";

import { AuthProvider } from "./context/AuthContext";

const App = () => {
  return (
      <Router>
        <AuthProvider>
            <Routes>
                <Route exact path="/" element={<Login/>}/>
                <Route exact path="/register" element={<Register/>}/>
                <Route exact path="/document-submission" element={<DocumentSubmission/>}/>
                <Route exact path="/verify-documents" element={<VerifyDocs/>}/>
                <Route exact path="/detailed-doc/:email" element={<UserDocuments/>}/>
                <Route
                  path="/main-page"
                  element={
                    <PrivateRoute>
                      <MainPage />
                    </PrivateRoute>
                  }
                />
                <Route exact path="/reset-password" element={<ResetPassword/>}/>
            </Routes>
          </AuthProvider>
      </Router>
  );
};
export default App;
// class App extends React.Component(){
//   state = {details: [], }

//   componentDidMount(){
//     let data; 
//     axios.get('http://localhost:8000')
//     .then(res=>{
//       data = res.data
//       this.setState({
//         details: data
//       });
//     }).catch(err=>{
//       console.log(err);
//     })
//   }
//   render(){
//     return(
//       <div>
//         <header>Данные из Django</header>
//         <hr></hr>
//         {this.state.details.map((output,id) => {
//           <div key={id}>
//             <div>
//               <h2>{output.first_name}</h2>
//               <p>{output.last_name}</p>
//             </div>
//           </div>
//         })}
//       </div>
//     )
//   }
// }

// function App() {
//   return (
//     <div>
//         <Login/>
//     </div>
//   );
// }
