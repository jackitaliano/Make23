import React, { Component } from "react";
import { Button } from '@mui/material';

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

const recordingIntervalSec = 10;
const recordingIntervalMS = recordingIntervalSec * 1000;


export default class Recorder extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isActive: false,
    }

    this.mediaStream = null;
    this.mediaRecorder = null;
    this.intervalId = null;
    this.chunks = [];

    this.constraintObj = {
      audio: {
        sampleRate: 44100,
        bitsPerSecond: 16,
        channelCount: 1
      },
      video: false
    };

    this.openMediaStream = this.openMediaStream.bind(this);
    this.closeMediaStream = this.closeMediaStream.bind(this);
    this.sendData = this.sendData.bind(this);
    this.openMediaRecorder = this.openMediaRecorder.bind(this);
    this.recordVideoChunk = this.recordVideoChunk.bind(this);
    this.startMediaRecorder = this.startMediaRecorder.bind(this);
    this.stopMediaRecorder = this.stopMediaRecorder.bind(this);
  }
  
  async openMediaStream() {
    return navigator.mediaDevices.getUserMedia(this.constraintObj).then((mediaStreamObj) => {
      this.mediaStream = mediaStreamObj;
      return this.mediaStream;
    })
  }

  closeMediaStream() {
    this.mediaStream.getTracks().forEach(function(track) {
      if (track.readyState == 'live') {
          track.stop();
      }
    });
    this.mediaRecorder = null;
  }

  sendData(blob) {
    let csrftoken = getCookie('csrftoken');
    var url = '/api/audio'

    let formData = new FormData();
    formData.append('audio_file', blob, 'audio.webm');
    formData.append('note_id', this.props.noteId)
    console.log("Transcripting audio...");
    
    fetch(url, {
      method: 'POST',
      headers: { 
        'X-CSRFToken': csrftoken,
      },
      body: formData
    })
    .then((response => response.json()))
    .then((data) => {
      console.log("Updating note page...")
      this.props.updateParent()
    })
    .catch(error => {
      console.log(error);
    });
  }

  openMediaRecorder() {
    this.mediaRecorder = new MediaRecorder(this.mediaStream);
    const chunks = [];
    this.mediaRecorder.ondataavailable = e => chunks.push(e.data);
    this.mediaRecorder.onstop = e => this.sendData(new Blob(chunks, {type: "audio/webm"}));
  }

  recordVideoChunk() {
    this.openMediaRecorder();
    this.mediaRecorder.start();
    setTimeout(() => {
      if(this.state.isActive) {
        this.mediaRecorder.stop();
        this.recordVideoChunk(this.mediaStream);
      }
    }, recordingIntervalMS);
  }

  startMediaRecorder() {
    this.openMediaStream().then(() => {
      this.setState({
        isActive: true
      })
      this.recordVideoChunk();
    });
  }

  stopMediaRecorder() {
    console.log("Stopping media recorder...");    

    this.setState({
      isActive: false
    })
    
    this.mediaRecorder.stop();
    this.closeMediaStream();
  }

  render() {
    return (
      <div>
          <Button
          color={this.state.isActive ? "error" : "success"}
          variant={this.state.isActive ? "outlined" : "contained"}
          onClick={this.state.isActive ? this.stopMediaRecorder : this.startMediaRecorder}
          >
          {this.state.isActive ? "Stop" : "Start"}
          </Button>
      </div>
    );
  }
}
  
