import React from 'react';
import { SignIn } from "features/user";
import { connect } from 'common/modules/commonAPI';


export default function Home(){
    const handleClick = e => {
        e.preventDefault()
        alert(' Home Click ')
        connect()
        .then(res => {alert(`접속성공 : ${res.data.connection}`)})
        .catch(err => {alert(`접속 실패: ${err}`)})
    }
    return (<div>
        <button onClick={handleClick} >Connection</button>
        <SignIn/>
        
    </div>)
}
   