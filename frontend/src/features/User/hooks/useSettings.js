import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router';
import { updateUserSettings } from '../api/userApi';

import { updateUserSuccess } from '../redux/authActions';

export const useSettings = () => {
  const navigate = useNavigate();

  const dispatch = useDispatch();

  const { user } = useSelector((state) => state.auth);

  const initialForm = {
    first_name: '',

    last_name: '',

    email: '',

    phone_number: '',
  };

  const [formData, setFormData] = useState(initialForm);

  /* ----------------------------

     2. Синхронизируем redux → form

  ----------------------------- */

  useEffect(() => {
    if (user && Object.keys(user).length > 0) {
      setFormData({
        first_name: user.first_name || '',

        last_name: user.last_name || '',

        email: user.email || '',

        phone_number: user.phone_number || '',
      });
    }
  }, [user]);

  /* ----------------------------

     Handlers

  ----------------------------- */

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,

      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // не мутируем state

    const payload = { ...formData };

    if (!payload.phone_number) {
      delete payload.phone_number;
    }

    try {
      const response = await updateUserSettings(payload);
      console.log(response);

      if (response.status === 200) {
        dispatch(updateUserSuccess(response.data));

        navigate('/home');
      }
    } catch (error) {
      console.error('Update error:', error);
    }
  };

  return {
    handleSubmit,
    formData,
    handleChange,
  };
};
