import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { connect } from './commonAPI';

const initialState = {
  server: '',
  header: {},
};

export const connectAsync = createAsyncThunk(
  'common/connect',
  async (amount) => {
    const response = await connect(amount);
    // The value we return becomes the `fulfilled` action payload
    return response.data;
  }
);

export const commonSlice = createSlice({
  name: "server",
  initialState,
  reducers: {
    getServer: (state) => {
      state.value = initialState['server'];
    },
    getHeader: (state) => {
      state.value = initialState['header'];
    },
  },
});

export const { getServer, getHeader } = commonSlice.actions;
export default commonSlice.reducer;