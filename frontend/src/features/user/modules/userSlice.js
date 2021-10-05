const initialState = {users:[], user:{}}
export const addUserAction = user => ({type: 'ADD_USER', payload: user})
export const removeUserAction = email => ({type: 'REMOVE_USER', payload: email})
const userReducer = (state = initialState, action)  => {
    switch(action.type){
        case 'ADD_USER': return {...state, users:[...state.users, action.payload]}
        case 'REMOVE_USER': return {...state, users:state.users.filter(user => user.email != action.payload)}
        default : return state
    }
}
export default userReducer