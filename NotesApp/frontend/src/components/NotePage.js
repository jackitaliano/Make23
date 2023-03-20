import React, { Component } from "react";
import { Grid, Box, Button, Accordion, AccordionDetails, AccordionSummary} from '@mui/material';
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
    this.getNote = this.getNote.bind(this);
    this.takeNotes= this.takeNotes.bind(this);
    this.update = this.update.bind(this);

    this.getNote();
  }

  getNote(){
    console.log("getting notes");
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
      }); 
    });
  }

  takeNotes(){
    console.log("taking notes");
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
      }); 
  });
  }

  update() {
    console.log("test update");
    this.getNote();
  }

  render() {
    return (
      <Box mt={2} px={2}>
      <Grid container spacing={2}>
        <Grid item xs={12} s={6} md={6}>
          <Box>
            <Recorder updateParent={this.update}/>
            <TranscriptCard body={this.state.transcript}/>
          </Box>
        </Grid>
        <Grid item xs={12} s={6} md={6}>
          <Box>
            <Button color="primary" variant="contained" onClick={this.takeNotes}>
            Take notes
            </Button>
            <NoteCard body={this.state.notes}/>
          </Box>
        </Grid>
      </Grid>
      </Box>
    );
  }
}