import React, { Component } from "react";
import { Card, CardContent, Typography, TextField } from '@mui/material';
import ReactMarkdown from 'react-markdown'


export default class NoteCard extends Component {
  constructor(props) {
      super(props);
      this.state = {
        "body": this.props.body
      }
      
      this.handleBodyChange = this.handleBodyChange.bind(this);
  }

  handleBodyChange(e){
    this.setState({
      body: e.target.value
    });
  }

  componentDidUpdate(prevProps) {
    if (prevProps.body !== this.props.body) {
      this.setState({
        "body": this.props.body
      })
    }
  }
  
  render() {
    return (
      <div>
      <Card sx={{ minWidth: 275 }}>
        <CardContent>
          <Typography variant="h3" color="text.primary" gutterBottom>
            Notes
          </Typography>
          <hr/>
        <Typography component={'span'} style={{width: '100%'}}>
            <ReactMarkdown>{this.state.body}</ReactMarkdown>
        </Typography>
        </CardContent>
    </Card>
    </div>
    );
}
}