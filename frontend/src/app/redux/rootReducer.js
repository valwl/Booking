import { combineReducers } from 'redux';
import authReducer from '../../features/User/redux/authReducer';
import bookingReducer from '../../features/Booking/redux/booking/bookingReducer';
import timerReducer from '../../features/Booking/redux/timer/timerReducer';

const rootReducer = combineReducers({
  auth: authReducer,
});

export default rootReducer;
