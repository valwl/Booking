import React from 'react';
import { Link } from 'react-router-dom';
import styles from './AboutUs.module.scss';
import saganoForest from './sagradaFamilia2.jpg';

const AboutUs = () => {
  return (
    <div className={styles.aboutUsContainer}>
      <img src={saganoForest} alt="About Us" className={styles.aboutUsImage} />
      <div className={styles.aboutUsContent}>
        <h1>Welcome to Our Unique Booking Service</h1>
        <p>
          Discover exceptional apartments across the globe, each offering a
          unique experience tailored to your needs. Our company is dedicated to
          providing you with the most distinctive and unforgettable stays,
          whether you are traveling for leisure or business. We believe in
          offering not just a place to stay, but an experience that stays with
          you long after your journey.
        </p>
      </div>
      <Link to="/apartments" className={styles.aboutUsLink}>
        Go to Apartment Selection
      </Link>
    </div>
  );
};

export default AboutUs;
