import React from 'react';
import { Link } from 'react-router-dom';
import styles from './SaveBooking.module.scss';
import saganoForestImg from './saganoForest.jpeg';

const SaveBooking = () => {
  return (
    <div className={styles.saveBookingContainer}>
      <img
        src={saganoForestImg}
        alt="Save Booking"
        className={styles.saveBookingImage}
      />
      <div className={styles.saveBookingContent}>
        <h1>Secure Your Stay with Confidence</h1>
        <p>
          Our state-of-the-art booking system ensures that your reservations are
          not only easy to make but also highly secure. We prioritize your
          safety and convenience, so you can focus on enjoying your trip. Trust
          us to handle your bookings with the utmost care, providing you with
          peace of mind every step of the way.
        </p>
      </div>
      <button>
        Go to Apartment Selection
      </button>

      
    </div>
  );
};

export default SaveBooking;
