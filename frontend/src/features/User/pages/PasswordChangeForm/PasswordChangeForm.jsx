import React from 'react';

import styles from './PasswordChangeForm.module.scss';
import { usePasswordChange } from '../../hooks/usePasswordChange';

const PasswordChangeForm = () => {
  const { formData, handleChange, handleSubmit } = usePasswordChange();

  return (
    <div className={styles.pageStyle}>
      <form onSubmit={handleSubmit} className={styles.formContainer}>
        <h2>Password change form</h2>
        <div>
          <input
            type="text"
            name="new_password"
            value={formData.new_password}
            onChange={handleChange}
            className={styles.inputField}
            placeholder="password"
          />
        </div>

        <div>
          <input
            type="text"
            name="new_password_confirm"
            value={formData.new_password_confirm}
            onChange={handleChange}
            className={styles.inputField}
            placeholder="confirm password "
          />
        </div>
        <button type="submit" className={styles.submitButton}>
          submit
        </button>
      </form>
    </div>
  );
};

export default PasswordChangeForm;
