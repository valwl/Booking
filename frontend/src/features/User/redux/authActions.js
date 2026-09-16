import axios from 'axios';

export const login = (username, password) => async (dispatch) => {
  try {
    const response = await axios.post('/api/user_api/login/', {
      username,
      password,
    });
    console.log('Response:', response);
    dispatch({ type: 'USER_LOGIN_SUCCESS', payload: response.data });
    return response;
  } catch (error) {
    dispatch({ type: 'AUTH_ERROR', payload: { error: error.message } });
  }
};

export const userRegister = (userData) => {
  return async (dispatch) => {
    try {
      const response = await axios.post(
        '/api/user_api/register/',
        userData,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      console.log('Response:', response);

      if (response.status === 201) {
        dispatch({ type: 'USER_REGISTER_SUCCESS', payload: response.data });
        return response;
      } else {
        console.log('Registration failed with status:', response.status);
        return { status: response.status };
      }
    } catch (error) {
      console.error('Error occurred:', error);
      if (error.response) {
        console.error('Response data:', error.response.data);
      } else if (error.request) {
        console.error('Request:', error.request);
      } else {
        console.error('Error message:', error.message);
      }
      console.error('Error config:', error.config);
      return null;
    }
  };
};

export const logoutUser = () => async (dispatch, getState) => {
  const refresh = localStorage.getItem('refreshToken');
  const access = localStorage.getItem('accessToken');

  try {
    if (refresh) {
      await axios.post(
        '/api/user_api/logout/',
        { refresh },
        {
          headers: {
            Authorization: `Bearer ${access}`,
          },
        }
      );
    }
  } catch (error) {
    console.warn('Logout error (ignired):', error);
  } finally {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');

    dispatch({ type: 'USER_LOGOUT' });
  }
};

export const refreshAccessToken = (id) => async (dispatch) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    const refrechToken = localStorage.getItem('refrechToken');

    if (!accessToken) throw new Error('Access token not found');

    const response = await axios.post(
      '/api/user_api/token/refresh/',
      { refresh: refrechToken }
    );

    const { access } = response.data;
    console.log(response.data);
    dispatch({ type: 'TOKEN_REFRESH_SUCCESS', payload: access });
    localStorage.setItem('accessToken', access);
    return access;
  } catch (error) {
    console.error('Error refreshing access token:', error);
    dispatch(logoutUser());
  }
};

export const updateUserSuccess = (updateUser) => {
  return {
    type: 'USER_UPDATE_SUCCESS',
    payload: updateUser,
  };
};
