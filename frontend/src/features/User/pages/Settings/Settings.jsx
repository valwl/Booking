import React from 'react';

import { Link } from 'react-router-dom';

import styles from './Settings.module.scss';
import { useSettings } from '../../hooks/useSettings';

const Settings = () => {
  const { handleSubmit, formData, handleChange } = useSettings();

  return (
    <div className={styles.settingsContainer}>
      <form onSubmit={handleSubmit} className={styles.settingsForm}>
        <h2>User Change Form</h2>

        <input
          type="text"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Email"
        />

        <input
          type="text"
          name="phone_number"
          value={formData.phone_number}
          onChange={handleChange}
          placeholder="Phone number"
        />

        <input
          type="text"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
          placeholder="First name"
        />

        <input
          type="text"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
          placeholder="Last name"
        />

        <Link to="/passwordChange/" className={styles.settingsLink}>
          Change password
        </Link>

        <button type="submit" className={styles.settingsSubmitButton}>
          Save changes
        </button>
      </form>
    </div>
  );
};

export default Settings;
