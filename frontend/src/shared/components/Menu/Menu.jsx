import React from 'react';
import { Link } from 'react-router-dom';

import styles from './Menu.module.scss';

import { useMenu } from './useMenu';

const Menu = () => {
  const { isAuthenticated, setIsOpen, isOpen, handleLogout, handleClose } =
    useMenu();

  return (
    <nav className={styles.menu}>
      <ul className={styles.menu_list}>
        <li>
          <Link to="home" className={styles.linkMenuStyle}>
            Home
          </Link>
        </li>

        <li>
          <p>
            Locations
          </p>
        </li>
        <li>
          <p>
            Apartments
          </p>
        </li>
        <li>
          <Link to="/SaveBooking" className={styles.linkMenuStyle}>
            save booking
          </Link>
        </li>
        <li>
          <Link to="AboutUS" className={styles.linkMenuStyle}>
            About us
          </Link>
        </li>

        {isAuthenticated ? (
          <li className={styles.user_menu} onMouseEnter={() => setIsOpen(true)}>
            <span> user menu </span>
            {isOpen && (
              <ul className={styles.dropdown_menu}>
                <li>
                  <Link to="/settings" className={styles.linkMenuStyle}>
                    settings
                  </Link>
                </li>
                <li>
                  <p>
                    my apartment
                  </p>
                </li>
                <li>
                  <p>
                    my bookings
                  </p>
                </li>
                <li onClick={handleLogout}>logout</li>
                <li onClick={handleClose} className={styles.close_menu}>
                  +
                </li>
              </ul>
            )}
          </li>
        ) : (
          <li>
            <Link to="/Login" className={styles.linkMenuStyle}>
              Login
            </Link>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default Menu;
