import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router';
import { login } from '../redux/authActions';

export const useLogin = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { bookingData } = useSelector((state) => state.booking);
  console.log(bookingData);

  const initialData = {
    username: '',
    password: '',
  };

  const [formData, setFormData] = useState(initialData);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await dispatch(
        login(formData.username, formData.password)
      );
      console.log('response data', response);
      if (response && response.status === 200) {
        console.log(bookingData);
        if (
          bookingData &&
          bookingData.checkin_day &&
          bookingData.checkout_day
        ) {
          navigate('/bookingConfirm', {
            state: { formData: bookingData },
          });
        } else {
          navigate('/home');
        }

        console.log('welcome inside of the system');
      }
    } catch (error) {
      console.error('information about error', error);
    }

    setFormData(initialData);
  };

  return {
    handleLogin,
    formData,
    handleChange,
  };
};
