import React from "react";
import {Route,Switch, Redirect} from 'react-router-dom'
import { Navi, Counter, Todo } from "common";
import { Linear, NonLinear } from "datastructure";
import { BackTracking, BruteForce, DivideConquer, DynamicProgramming, Greedy } from "algorithm";
import { Mathematics } from "datastructure";
import {Home} from 'common/index'

const App = () => (
  <>
  <Navi/>
  <Switch>
    <Route exact path = '/' component = {Home}/>
    <Redirect from='/home' to= { '/' }/>
    <Route exact path = '/counter' component = {Counter}/>
    <Route exact path = '/todo' component = {Todo}/>
    <Route exact path = '/mathematics' component = {Mathematics}/>
    <Route exact path = '/linear' component = {Linear}/>
    <Route exact path = '/nonLinear' component = {NonLinear}/>
    <Route exact path = '/backTracking' component = {BackTracking}/>
    <Route exact path = '/bruteForce' component = {BruteForce}/>
    <Route exact path = '/divideConquer' component = {DivideConquer}/>
    <Route exact path = '/dynamicProgramming' component = {DynamicProgramming}/>
    <Route exact path = '/greedy' component = {Greedy}/>
  </Switch>
  </>
)
export default App