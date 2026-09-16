import { useState, useEffect } from 'react';

export const useHome = () => {
  const [images, setImages] = useState([]);

  useEffect(() => {

   const mockImages = [
      "https://unsplash.com",
      "https://unsplash.com",
      "https://unsplash.com"
    ];

    setImages(mockImages);
  }, []);

  return {
    images,
  };
};
