import React from 'react';
import { Link } from 'react-router-dom';

import style from './UserRegisterForm.module.scss';
import { useRegister } from '../../hooks/useRegister';

const UserRegisterForm = () => {
  const { handleSubmit, handleChange, userData } = useRegister();

  return (
    <div className={style.page_style}>
      <div className={style.register_form}>
        <h1>Register</h1>
        <form onSubmit={handleSubmit}>
          <div className={style.txt_field}>
            <input
              type="email"
              name="email"
              value={userData.email}
              onChange={handleChange}
            />
            <span></span>
            <label>email:</label>
          </div>

          <div className={style.txt_field}>
            <input
              type="text"
              name="phone_number"
              value={userData.phone_number}
              onChange={handleChange}
            />
            <span></span>
            <label>phone_number:</label>
          </div>

          <div className={style.txt_field}>
            <input
              type="text"
              name="first_name"
              value={userData.first_name}
              onChange={handleChange}
              required
            />
            <span></span>
            <label>first_name:</label>
          </div>

          <div className={style.txt_field}>
            <input
              type="text"
              name="last_name"
              value={userData.last_name}
              onChange={handleChange}
              required
            />
            <span></span>
            <label>last_name:</label>
          </div>

          <div className={style.txt_field}>
            <input
              type="password"
              name="password"
              value={userData.password}
              onChange={handleChange}
              required
            />
            <span></span>
            <label>password:</label>
          </div>

          <input
            name="submit"
            type="Submit"
            value="Register"
            onChange={handleChange}
          ></input>

          <div className={style.signup_link}>
            Alredady have an account?
            <Link to="/login" className={style.Link}>
              Login
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserRegisterForm;
