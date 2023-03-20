import React, { Component } from "react";
import { createRoot } from 'react-dom/client';
import HomePage from "./HomePage";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div style={{width: '100%', height: '100vh', overflow:'auto'}}>
        <HomePage />
      </div>
    );
  }
}

const container = document.getElementById('app');
const root = createRoot(container); 
root.render(<App />);