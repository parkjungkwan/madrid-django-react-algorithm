import React from "react";
import { UserJoin, UserList } from "features/user";



export default function SignUp() {
    return(
        <div>
            <h1>회원가입</h1>
        <UserJoin/>
        <UserList/>
        </div>
    )
    
}