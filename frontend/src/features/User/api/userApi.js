import api from '../../../shared/lib/axiosInstance';

export const passwordChange = (formData) => {
  const response = api.post(`/user_api/user/password/change/`, formData);
  return response;
};

export const updateUserSettings = async (payload) => {
  const response = await api.patch(
    '/user_api/user/update/',

    payload
  );
  return response;
};

export const getUserData = async () => {
  const response = await api.get(`/user_api/user/me/`);
  return response;
};
