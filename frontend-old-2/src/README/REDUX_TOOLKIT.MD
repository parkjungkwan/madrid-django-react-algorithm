https://redux-toolkit.js.org/api/createAsyncThunk

*** Overview

A function that accepts a Redux action type string and a callback function that should return a promise. 
It generates promise lifecycle action types based on the action type prefix that you pass in, 
and returns a thunk action creator that will run the promise callback and 
dispatch the lifecycle actions based on the returned promise.

This abstracts the standard recommended approach for handling async request lifecycles.

It does not generate any reducer functions, since it does not know what data you're fetching, 
how you want to track loading state, or how the data you return needs to be processed. 
You should write your own reducer logic that handles these actions, 
with whatever loading state and processing logic is appropriate for your own app.

*** TIP

Redux Toolkit's RTK Query data fetching API is a purpose built data fetching and caching solution for Redux apps, 
and can eliminate the need to write any thunks or reducers to manage data fetching. 
We encourage you to try it out and see if it can help simplify the data fetching code in your own apps!

Parameters#
createAsyncThunk accepts three parameters: a string action type value, a payloadCreator callback, and an options object.

type#
A string that will be used to generate additional Redux action type constants, representing the lifecycle of an async request:

For example, a type argument of 'users/requestStatus' will generate these action types:

pending: 'users/requestStatus/pending'
fulfilled: 'users/requestStatus/fulfilled'
rejected: 'users/requestStatus/rejected'
payloadCreator#
A callback function that should return a promise containing the result of some asynchronous logic. It may also return a value synchronously. If there is an error, it should either return a rejected promise containing an Error instance or a plain value such as a descriptive error message or otherwise a resolved promise with a RejectWithValue argument as returned by the thunkAPI.rejectWithValue function.

The payloadCreator function can contain whatever logic you need to calculate an appropriate result. This could include a standard AJAX data fetch request, multiple AJAX calls with the results combined into a final value, interactions with React Native AsyncStorage, and so on.

The payloadCreator function will be called with two arguments:

arg: a single value, containing the first parameter that was passed to the thunk action creator when it was dispatched. This is useful for passing in values like item IDs that may be needed as part of the request. If you need to pass in multiple values, pass them together in an object when you dispatch the thunk, like dispatch(fetchUsers({status: 'active', sortBy: 'name'})).
thunkAPI: an object containing all of the parameters that are normally passed to a Redux thunk function, as well as additional options:
dispatch: the Redux store dispatch method
getState: the Redux store getState method
extra: the "extra argument" given to the thunk middleware on setup, if available
requestId: a unique string ID value that was automatically generated to identify this request sequence
signal: an AbortController.signal object that may be used to see if another part of the app logic has marked this request as needing cancelation.
rejectWithValue(value, [meta]): rejectWithValue is a utility function that you can return (or throw) in your action creator to return a rejected response with a defined payload and meta. It will pass whatever value you give it and return it in the payload of the rejected action. If you also pass in a meta, it will be merged with the existing rejectedAction.meta.
fulfillWithValue(value, meta): fulfillWithValue is a utility function that you can return in your action creator to fulfill with a value while having the ability of adding to fulfilledAction.meta.
The logic in the payloadCreator function may use any of these values as needed to calculate the result.

Options#
An object with the following optional fields:

condition(arg, { getState, extra } ): boolean: a callback that can be used to skip execution of the payload creator and all action dispatches, if desired. See Canceling Before Execution for a complete description.
dispatchConditionRejection: if condition() returns false, the default behavior is that no actions will be dispatched at all. If you still want a "rejected" action to be dispatched when the thunk was canceled, set this flag to true.
idGenerator(): string: a function to use when generating the requestId for the request sequence. Defaults to use nanoid.
serializeError(error: unknown) => any to replace the internal miniSerializeError method with your own serialization logic.
getPendingMeta({ arg, requestId }, { getState, extra }): any: a function to create an object that will be merged into the pendingAction.meta field.
Return Value#
createAsyncThunk returns a standard Redux thunk action creator. The thunk action creator function will have plain action creators for the pending, fulfilled, and rejected cases attached as nested fields.

Using the fetchUserById example above, createAsyncThunk will generate four functions:

fetchUserById, the thunk action creator that kicks off the async payload callback you wrote
fetchUserById.pending, an action creator that dispatches an 'users/fetchByIdStatus/pending' action
fetchUserById.fulfilled, an action creator that dispatches an 'users/fetchByIdStatus/fulfilled' action
fetchUserById.rejected, an action creator that dispatches an 'users/fetchByIdStatus/rejected' action
When dispatched, the thunk will:

dispatch the pending action
call the payloadCreator callback and wait for the returned promise to settle
when the promise settles:
if the promise resolved successfully, dispatch the fulfilled action with the promise value as action.payload
if the promise resolved with a rejectWithValue(value) return value, dispatch the rejected action with the value passed into action.payload and 'Rejected' as action.error.message
if the promise failed and was not handled with rejectWithValue, dispatch the rejected action with a serialized version of the error value as action.error
Return a fulfilled promise containing the final dispatched action (either the fulfilled or rejected action object)
