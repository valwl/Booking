import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router';
import { userRegister } from '../redux/authActions';

export const useRegister = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const currentState = useSelector((state) => state.auth);
  const initialFormData = {
    email: '',
    phone_number: ' ',
    password: '',
    first_name: '',
    last_name: '',
  };
  const [userData, setUserData] = useState(initialFormData);

  const handleChange = (e) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const serializedUserData = {
      ...userData,
      phone_number: userData.phone_number.trim(),
    };
    try {
      const response = await dispatch(userRegister(userData));
      if (response && response.status === 201) {
        navigate('/home');
      } else {
        alert('sory some error with request data please try again');
      }
    } catch (error) {
      console.error('Errorin handleSubmit:', error);
      alert('An unexpected error with request data please try again');
    }
    setUserData(initialFormData);
  };

  useEffect(() => {
    console.log('current state', currentState);
  }, [currentState]);

  return {
    handleSubmit,
    handleChange,
    userData,
  };
};
