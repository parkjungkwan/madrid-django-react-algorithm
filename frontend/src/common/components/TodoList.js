import React from "react";
import styled from 'styled-components'
export default function TodoList() {
    return ( 
        <TodoListDiv><h1>등록된 할일 목록이 없습니다.</h1></TodoListDiv>
    )
    
}
const TodoListDiv = styled.div`text-align: center;`