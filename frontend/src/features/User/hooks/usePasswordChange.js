import { useState } from 'react';
import { useNavigate } from 'react-router';
import { passwordChange } from '../api/userApi';

export const usePasswordChange = () => {
  const navigate = useNavigate();

  const initialData = {
    new_password: '',
    new_password_confirm: '',
  };
  const [formData, setFormData] = useState(initialData);

  const handleChange = async (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.new_password === formData.new_password_confirm) {
      try {
        const response = await passwordChange(formData);
        if (response.status === 204) {
          navigate('/home');
        }
        console.log(response);
      } catch (error) {
        console.error('error data:', error);
      }
    } else {
      alert('password didnt match please try again');
    }
  };

  return {
    formData,
    handleChange,
    handleSubmit,
  };
};
