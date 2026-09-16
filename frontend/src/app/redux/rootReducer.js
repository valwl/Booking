import { combineReducers } from 'redux';
import authReducer from '../../features/User/redux/authReducer';

const rootReducer = combineReducers({
  auth: authReducer,
});

export default rootReducer;
