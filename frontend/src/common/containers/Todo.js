import React, {useState} from "react";
import styled from 'styled-components'
export default function Todo() {
    const [todo, setTodo] = useState('')
    let temp = ''
    const add = e =>{
        e.preventDefault()
        temp = e.target.value
     }
    const del = e =>{
        e.preventDefault()
        setTodo('')
    }
    const submitForm = e =>{
        e.preventDefault()
        setTodo(temp)
        document.getElementById('todo-input').value = ''
    }

    return(
        <form onSubmit={submitForm} method='POST'>
        <CounterDiv>
            <input onChange={add} type='text' id='todo-input'/>
            <input type='submit' value='ADD' /><br/>
            <span>{todo}</span>
            <input onClick={del} type='button' value='DEL'/>
        </CounterDiv></form>
    )
}

const CounterDiv = styled.div`text-align: center;`