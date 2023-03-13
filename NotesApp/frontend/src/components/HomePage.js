import React, { Component } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Redirect,
} from "react-router-dom";
import NotePage from "./NotePage";

export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
    <Router>
      <Routes>
        <Route path='/' element={<NotePage/>}/>
      </Routes>
    </Router>
    );
  }
}