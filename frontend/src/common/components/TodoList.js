import React from "react";
import styled from 'styled-components'
import { useSelector } from 'react-redux'
export default function TodoList() {
    const todos = useSelector( state => state.todoReducer.todos )
    return ( 
        <TodoListDiv>
        {todos.length === 0 && (<h1>등록된 할일 목록이 없습니다.</h1>)}
        {todos.length !== 0 && (<h1>{todos.length} 개의 할일 목록 있습니다.</h1>)}
        </TodoListDiv>
    )
    
}
const TodoListDiv = styled.div`text-align: center;`