import React from "react";
import { Link } from 'react-router-dom';
import styled from 'styled-components';


const Navi = () => (
    <NaviDiv>
     
     <NaviList>
            <NaviItem><Link to='/counter'style={{textDecorationLine:'none',color:'black'}}><strong>Counter</strong></Link></NaviItem>
            <NaviItem><Link to='/math'style={{textDecorationLine:'none',color:'black'}}><strong>(0차원) 수학</strong></Link></NaviItem>
            <NaviItem><Link to='/linear'style={{textDecorationLine:'none',color:'black'}}><strong>(1차원) 선형</strong></Link></NaviItem>
            <NaviItem><Link to="/nonlinear"style={{textDecorationLine:'none',color:'black'}}><strong>(2차원) 비선형</strong></Link></NaviItem>
            <NaviItem><Link to="/bruteForce"style={{textDecorationLine:'none',color:'black'}}><strong>Brute Force 완전탐색</strong></Link></NaviItem>
            <NaviItem><Link to="/divideConquer"style={{textDecorationLine:'none',color:'black'}}><strong>Divide & Conquer 분할정복</strong></Link></NaviItem>
            <NaviItem><Link to="/greedy"style={{textDecorationLine:'none',color:'black'}}><strong>Greedy</strong></Link></NaviItem>
            <NaviItem><Link to="/dynamicProgramming"style={{textDecorationLine:'none',color:'black'}}><strong>Dynamic Programming 동적</strong></Link></NaviItem>
            <NaviItem><Link to="/backTracking "style={{textDecorationLine:'none',color:'black'}}><strong>Back Tracking 백트래킹</strong></Link></NaviItem>
        </NaviList>
    </NaviDiv>
)
export default Navi




const NaviDiv = styled.div`
    padding-bottom: 30px;
    margin-bottom: 100px;
    
`
const NaviList = styled.ul`
    display: flex;
    width: min-content;
    height:10px;
    margin: 30px
    
`

const NaviItem = styled.li`
    width: 110px;
    color: none;
    font-family: "ls";
    font-size: 1.5em;
    list-style: none;
    `