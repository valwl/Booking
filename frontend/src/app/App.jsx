import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';

import Home from '../Pages/Home/Home.jsx';
import AboutUs from '../Pages/AboutUs/AboutUs';

import SaveBooking from '../Pages/SaveBooking/SaveBooking';

import Menu from '../shared/components/Menu/Menu.jsx';
import Footer from '../shared/components/Footer/Footer.jsx';
import './styles/App.css';


import UserLoginForm from '../features/User/pages/UserLoginForm/userLoginForm.jsx';
import UserRegisterForm from '../features/User/pages/UserRegisterForm/UserRegisterForm.jsx';
import PasswordChangeForm from '../features/User/pages/PasswordChangeForm/PasswordChangeForm.jsx';
import Settings from '../features/User/pages/Settings/Settings.jsx';


function App() {
  return (
    <div className="App">
      <Menu />
      <ToastContainer />
      <Routes>
        <Route path="/" element={<Navigate replace to="/home" />} />
        <Route path="/home" exact element={<Home />} />
        <Route path="/AboutUS" exact Component={AboutUs} />
        <Route path="/SaveBooking" exact Component={SaveBooking} />

        <Route path="/Login" element={<UserLoginForm />} />
        <Route path="/register" element={<UserRegisterForm />} />
        <Route path="/passwordChange" element={<PasswordChangeForm />} />
        <Route path="/settings" element={<Settings />} />


      </Routes>
      <Footer />
    </div>
  );
}

export default App;



