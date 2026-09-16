const initialState = {
  isAuthenticated: false,
  token: '',
  refresh_token: '',
  user: {
    email: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    id: '',
  },
  error: '',
};

const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'USER_REGISTER_SUCCESS':
    case 'USER_LOGIN_SUCCESS':
      const { access, refresh } = action.payload.tokens;
      const { email, first_name, last_name, phone_number, id } =
        action.payload.user;
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      return {
        ...state,
        isAuthenticated: true,
        token: access,
        user: {
          email: email,
          first_name: first_name,
          last_name: last_name,
          phone_number: phone_number,
          id: id,
        },
        error: null,
      };

    case 'TOKEN_REFRESH_SUCCESS':
      localStorage.setItem('accessToken', action.payload.access);
      return {
        ...state,
        token: action.payload.access,
      };

    case 'USER_LOGOUT':
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      return {
        ...state,
        isAuthenticated: false,
        token: '',
        user: initialState.user,
        error: null,
      };

    case 'USER_UPDATE_SUCCESS':
      return {
        ...state,
        user: {
          ...state.user,
          ...action.payload,
        },
      };

    case 'AUTH_ERROR':
      return {
        ...state,
        error: action.payload,
      };

    default:
      return state;
  }
};

export default authReducer;
