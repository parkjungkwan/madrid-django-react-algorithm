import React, {useState} from "react";
import { useDispatch } from "react-redux";
import { v4 as uuidv4} from 'uuid'
import styled from 'styled-components'
import { addTodoAction } from "features/todos/modules/todoSlice";
export default function TodoInput() {
    const [todo, setTodo] = useState('')
    const dispatch = useDispatch()
    const submitForm = e =>{
        e.preventDefault()
        const newTodo = {
            id: uuidv4(),
            name: todo,
            complete: false
        }
        addTodo(newTodo)
        setTodo('')
    }

    const addTodo = todo => (dispatch(addTodoAction(todo)))
    const handleChange = e =>{
        e.preventDefault()
        setTodo(e.target.value)
     }
   
    return(
        <form onSubmit={submitForm} method='POST'>
        <CounterDiv>
            <input type='text' 
                    id='todo'
                    name = 'todo'
                    placeholder="할일 입력"
                    value = {todo}
                    onChange={handleChange} />
            <input type='submit' 
                    value='ADD' /><br/>
        </CounterDiv></form>
    )
}

const CounterDiv = styled.div`text-align: center;`