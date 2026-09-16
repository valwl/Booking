import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';
import styles from './BaseSlider.module.scss';

const BaseSlider = ({ images, activeSlide }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (activeSlide !== undefined) {
      setCurrentIndex(activeSlide);
    }
  }, [activeSlide]);

  const handleNextImage = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
  };

  const handlePrevImage = () => {
    setCurrentIndex(
      (prevIndex) => (prevIndex - 1 + images.length) % images.length
    );
  };

  return (
    <div className={styles.slider}>
      <div
        className={styles.imagesContainer}
        style={{ transform: `translateX(-${currentIndex * 100}%)` }}
      >
        {images.map((image, index) => (
          <div key={index} className={styles.slide}>
            <img
              src={image}
              alt={`Slide ${index + 1}`}
              className={styles.sliderImage}
            />
          </div>
        ))}
      </div>
      {images.length > 1 && (
        <div className={styles.navigation}>
          <button className={styles.prevButton} onClick={handlePrevImage}>
            <FaChevronLeft className={styles.icons} />
          </button>
          <button className={styles.nextButton} onClick={handleNextImage}>
            <FaChevronRight className={styles.icons} />
          </button>
        </div>
      )}
    </div>
  );
};

BaseSlider.propTypes = {
  images: PropTypes.arrayOf(PropTypes.string).isRequired,
  activeSlide: PropTypes.number,
};

export default BaseSlider;
