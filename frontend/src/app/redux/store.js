import { createStore, applyMiddleware } from 'redux';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { thunk } from 'redux-thunk';
import rootReducer from './rootReducer';

import { composeWithDevTools } from '@redux-devtools/extension';

const persistConfig = {
  key: 'root',
  storage: storage.default || storage,
  whitelist: ['auth'],
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

const composeEnhancers = composeWithDevTools(applyMiddleware(thunk));

const store = createStore(persistedReducer, composeEnhancers);

export const persistor = persistStore(store);

export default store;
