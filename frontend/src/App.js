import React from "react";
import { Route,Switch, Redirect } from 'react-router-dom'
import { Navi, Counter, Todo, SignUp } from "common";
import { Linear, NonLinear } from "datastructure";
import { BackTracking, BruteForce, DivideConquer, DynamicProgramming, Greedy } from "algorithm";
import { Mathematics } from "datastructure";
import { Home } from 'common'
import { createStore, combineReducers } from 'redux'
import { Provider } from 'react-redux'
import { todoReducer, userReducer  } from 'reducers'
const rootReducer = combineReducers({todoReducer, userReducer})
const store = createStore(rootReducer)
const App = () => (
    <Provider store={store}>
      <Navi/>
        <Switch>
          <Route exact path = '/' component = {Home}/>
          <Redirect from='/home' to= { '/' }/>
          <Route exact path = '/counter' component = {Counter}/>
          <Route exact path = '/todo' component = {Todo}/>
          <Route exact path = '/sign-up' component = {SignUp}/>
          <Route exact path = '/mathematics' component = {Mathematics}/>
          <Route exact path = '/linear' component = {Linear}/>
          <Route exact path = '/nonLinear' component = {NonLinear}/>
          <Route exact path = '/back-tracking' component = {BackTracking}/>
          <Route exact path = '/brute-force' component = {BruteForce}/>
          <Route exact path = '/divide-conquer' component = {DivideConquer}/>
          <Route exact path = '/dp' component = {DynamicProgramming}/>
          <Route exact path = '/greedy' component = {Greedy}/>
        </Switch>
    </Provider>
)
export default App