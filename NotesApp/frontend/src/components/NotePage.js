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
      noteId: this.props.noteId,
      transcript: "",
      notes: "",
    }
    this.getNote = this.getNote.bind(this);
    this.takeNotes= this.takeNotes.bind(this);
    this.update = this.update.bind(this);
    this.newNote = this.newNote.bind(this);

    this.getNote();
  }

  async getNote(){
    console.log("Getting notes...");
    var csrftoken = getCookie('csrftoken')
    var params = new URLSearchParams({"note_id": this.state.noteId})
    var url = '/api/note?' + params

    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrftoken
      },
    };

    return fetch(url, requestOptions)
    .then((response => response.json()))
    .then((data) => {
      this.setState({ 
        transcript: data.transcript,
        notes: data.notes,
      }); 
    });
  }

  async takeNotes(){
    console.log("Taking notes...");
    var csrftoken = getCookie('csrftoken')
    var url = '/api/take-notes';
    var formData = new FormData();
    formData.append("note_id", this.state.noteId)

    const requestOptions = {
      method: "POST",
      headers: {
        'X-CSRFToken': csrftoken
      },
      body: formData
    };

    fetch(url, requestOptions)
      .then((response => response.json()))
      .then((data) => {
        this.setState({ 
          transcript: data.transcript,
          notes: data.notes,
        })
      })
      .catch((error) => {
        console.log(error);
      });
  }

  async newNote() {
    console.log("Getting notes...");
    var csrftoken = getCookie('csrftoken')
    var params = new URLSearchParams({"note_id": "NEW"})
    var url = '/api/note?' + params

    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrftoken
      },
    };

    return fetch(url, requestOptions)
    .then((response => response.json()))
    .then((data) => {
      this.setState({ 
        noteId: data.note_id,
        transcript: data.transcript,
        notes: data.notes,
      }); 
    });
  }

  update() {
    this.getNote();
  }

  render() {
    return (
      <Box mt={2} px={2}>
      <Grid container spacing={2}>
        <Grid item xs={12} s={6} md={6}>
          <Box>
            <Recorder noteId={this.state.noteId} updateParent={this.update}/>
            <TranscriptCard body={this.state.transcript}/>
          </Box>
        </Grid>
        <Grid item xs={12} s={6} md={6}>
          <Grid container spacing={2}>
            <Grid item xs={11}>

            </Grid>
            <Grid item xs={1}>
              <Button color="secondary" variant="outlined" onClick={this.newNote}>
                New Note
              </Button>
            </Grid>
          </Grid>
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