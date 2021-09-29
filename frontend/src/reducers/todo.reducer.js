const initialState = {todos:[], todo:{}}
export const addTodoAction = todo => ({type: 'ADD_TODO', payload: todo})
const todoReducer = (state = initialState, action)  => {
    switch(action.type){
        case 'ADD_TODO': return {...state, todos:[...state.todos, action.payload]}
        default : return state
    }
}
export default todoReducer