import React, { useState } from 'react';
// import { useSelector, useDispatch } from 'react-redux';
// import {
//   decrement,
//   increment,
//   incrementByAmount,
//   incrementAsync,
//   incrementIfOdd,
//   selectCount,
// } from '../counterSlice';
import { Link } from 'react-router-dom'


export default function Navigation() {
  
  return (
    <div>
        <ul>
            <li><Link to="home">Home</Link></li>
            <li><Link to="/users/add">UserAdd</Link></li>
            <li><Link to="/users/detail">UserDetail</Link></li>
            <li><Link to="/users/list">UserList</Link></li>
            <li><Link to="/users/login">UserLogin</Link></li>
            <li><Link to="/users/modify">UserModify</Link></li>
            <li><Link to="/users/remove">UserRemove</Link></li>
        </ul>
    </div>
  );
}