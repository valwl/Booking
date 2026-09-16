import axios from 'axios';

import store from '../../app/redux/store';

import { logoutUser } from '../../features/User/redux/authActions';

/*

|--------------------------------------------------------------------------

| Base axios instance

|--------------------------------------------------------------------------

*/

export const publickApi = axios.create({
  baseURL: '/api',

  timeout: 10000,
});

const api = axios.create({
  baseURL: '/api',

  timeout: 10000,
});

/*

|--------------------------------------------------------------------------

| Request interceptor — DRY token attach

|--------------------------------------------------------------------------

*/

api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('accessToken');


    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },

  (error) => Promise.reject(error)
);

/*

|--------------------------------------------------------------------------

| Refresh control variables

|--------------------------------------------------------------------------

*/

let isRefreshing = false;

let failedQueue = [];

/*

|--------------------------------------------------------------------------

| Queue processor

|--------------------------------------------------------------------------

*/

const processQueue = (error, token = null) => {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) reject(error);
    else resolve(token);
  });

  failedQueue = [];
};

/*

|--------------------------------------------------------------------------

| Response interceptor — refresh & retry logic

|--------------------------------------------------------------------------

*/

api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;



    if (!error.response) {
      return Promise.reject(error);
    }

    const { status } = error.response;

    console.log('401 FROM:', originalRequest.url);



    if (status !== 401) {
      return Promise.reject(error);
    }



    if (originalRequest._retry) {
      store.dispatch(logoutUser());

      return Promise.reject(error);
    }



    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject });
      }).then((token) => {
        originalRequest.headers.Authorization = `Bearer ${token}`;

        return api(originalRequest);
      });
    }

    originalRequest._retry = true;

    isRefreshing = true;

    try {
      const refreshToken = localStorage.getItem('refreshToken');

      if (!refreshToken) {
        throw new Error('Refresh token missing');
      }



      const { data } = await axios.post(
        '/api/user_api/token/refresh/',

        { refresh: refreshToken }
      );

      const newAccessToken = data.access;



      localStorage.setItem('accessToken', newAccessToken);



      api.defaults.headers.Authorization = `Bearer ${newAccessToken}`;



      processQueue(null, newAccessToken);



      originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

      return api(originalRequest);
    } catch (refreshError) {
      processQueue(refreshError, null);

      store.dispatch(logoutUser());

      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export default api;
