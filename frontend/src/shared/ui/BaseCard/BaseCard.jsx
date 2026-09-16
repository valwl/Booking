import React, { useState } from 'react';
import styles from './BaseCard.module.scss';
import BaseSlider from '../../../shared/components/BaseSlider/BaseSlider';

const BaseCard = ({ title, images, onMoreDetails, children, backContent }) => {
  const [flipped, setFlipped] = useState(false);
  console.log(flipped);

  const handleFlip = (event) => {
    setFlipped((prevFlipped) => !prevFlipped);
  };

  return (
    <div
      className={`${styles.baseCard} ${
        !flipped ? styles.unFlipped : styles.flipped
      }`}
      onClick={handleFlip}
    >
      <div className={styles.cardFront}>
        <div
          className={styles.imageContainer}
          onClick={(e) => e.stopPropagation()}
        >
          <BaseSlider images={images} />
        </div>

        <div className={styles.baseCardContent}>
          <h3 className={styles.baseCardTitle}>{title}</h3>
          <button
            className={styles.baseCardButton}
            onClick={(e) => {
              e.stopPropagation();
              onMoreDetails();
            }}
          >
            Get More Info
          </button>
          {children}
        </div>
      </div>

      <div className={styles.cardBackend}>
        <div className={styles.cardBackContent}>
          <p>{backContent.slice(0, 100)}...</p>
          <button
            className={styles.baseCardButton}
            onClick={(e) => {
              e.stopPropagation();
              onMoreDetails();
            }}
          >
            Get More Info
          </button>
        </div>
      </div>
    </div>
  );
};

export default BaseCard;
