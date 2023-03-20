import ReactMarkdown from 'react-markdown'
import React, { Component } from "react";


export default class Markdown extends Component {
  constructor(props) {
      super(props);
  }
  
  render() {
    return (
        <ReactMarkdown>{this.props.text}</ReactMarkdown>
    );
}
}