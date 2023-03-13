import React, { Component } from "react";
import { Card, CardContent, Typography, TextField } from '@mui/material';

export default class TranscriptCard extends Component {
  constructor(props) {
      super(props);
      this.state = {
        "body": this.props.body
      }
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
            Transcript
          </Typography>
          <hr/>
        <Typography onChange={this.handleBodyChange}>
            {this.state.body}
        </Typography>
        </CardContent>
    </Card>
    </div>
    );
}
}