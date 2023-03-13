import React, { Component } from "react";
import { Grid, Container, Box, Button} from '@mui/material';
import NoteCard from "./Note";
import TranscriptCard from "./Transcript";
import Recorder from "./Recorder";

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

export default class NotePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      transcript: "",
      notes: "",
    }
    this.getNote()
    this.handleButtonClicked= this.handleButtonClicked.bind(this);
  }

  getNote(){
    var csrftoken = getCookie('csrftoken')
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrftoken
      }
    };

    fetch('/api/note', requestOptions)
    .then((response => response.json()))
    .then((data) => {
      this.setState({ 
        transcript: data.transcript,
        notes: data.notes,
      }, () => {
        console.log(this.state);
      }); 
    });
  }

  handleButtonClicked(){
    var csrftoken = getCookie('csrftoken')
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
        transcript: this.state.transcript,
        notes: this.state.notes
      }),
    };

    fetch('/api/take-notes', requestOptions)
    .then((response => response.json()))
    .then((data) => {
      this.setState({ 
        transcript: data.transcript,
        notes: data.notes,
      }, () => {
        console.log(this.state);
      }); 
  });
  }

  render() {
    return (
      <Box mt={2}>
      <Container maxWidth="xlg">
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Recorder/>
            </Grid>
            <Grid item xs={6}>
              <Button color="primary" variant="contained" onClick={this.handleButtonClicked}>
                  Take notes
              </Button>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={6}>
          <TranscriptCard body={this.state.transcript}/>
        </Grid>
        <Grid item xs={6}>
         <NoteCard body={this.state.notes}/>
        </Grid>
      </Grid>
      </Container>
      </Box>
    );
  }
}