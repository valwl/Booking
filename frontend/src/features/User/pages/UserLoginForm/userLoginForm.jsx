import React from 'react';

import { Link } from 'react-router-dom';

import styles from './UserLoginForm.module.scss';
import { useLogin } from '../../hooks/useLogin';

const UserLoginForm = () => {
  const { handleLogin, formData, handleChange } = useLogin();

  return (
    <div className={styles.page_style}>
      <div className={styles.login_form}>
        <h1>Sign up</h1>
        <form onSubmit={handleLogin} className={styles.form}>
          <div className={styles.txt_field}>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
            <span></span>
            <label>Login</label>
          </div>

          <div className={styles.txt_field}>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            <span></span>
            <label>Password</label>
          </div>

          <input
            name="submit"
            type="submit"
            value="Login"
            onChange={handleChange}
          ></input>

          <div className={styles.signup_link}>
            don't have an account?{' '}
            <Link to="/register" className={styles.Link}>
              Register
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserLoginForm;
