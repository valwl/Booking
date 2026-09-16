import { useNavigate } from 'react-router';
import { useSelector, useDispatch } from 'react-redux';
import { useState } from 'react';
import { logoutUser } from '../../../features/User/redux/authActions';

export const useMenu = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { isAuthenticated } = useSelector((state) => state.auth);
  const [isOpen, setIsOpen] = useState(false);

  const handleClose = () => {
    setIsOpen(false);
  };

  const handleLogout = () => {
    const response = dispatch(logoutUser());
    console.log('data:', response);
    handleClose();
    navigate('/home');
  };

  return {
    isAuthenticated,
    setIsOpen,
    isOpen,
    handleLogout,
    handleClose,
  };
};
