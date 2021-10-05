import { configureStore } from '@reduxjs/toolkit';
import counterReducer from 'features/counter/modules/counterSlice';
import commonReducer from 'common/modules/commonSlice';
import todoReducer from 'features/todos/modules/todoSlice';
export const store = configureStore({
  reducer: {
    counter: counterReducer,
    common: commonReducer,
    todos: todoReducer
  },
});
