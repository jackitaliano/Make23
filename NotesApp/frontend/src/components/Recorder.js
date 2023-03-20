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

  /*********************************
  getUserMedia returns a Promise
  resolve - returns a MediaStream Object
  reject returns one of the following errors
  AbortError - generic unknown cause
  NotAllowedError (SecurityError) - user rejected permissions
  NotFoundError - missing media track
  NotReadableError - user permissions given but hardware/OS error
  OverconstrainedError - constraint video settings preventing
  TypeError - audio: false, video: false
  *********************************/


export default class Recorder extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isActive: false,
    }

    this.mediaRecorder = null;
    this.chunks = [];
    this.audioSave = document.getElementById('audio2');

    this.constraintObj = {
      audio: {
        sampleRate: 44100,
        bitsPerSecond: 16,
        channelCount: 1
      },
      video: false
    };

    this.openMediaRecorder = this.openMediaRecorder.bind(this);
    this.startMediaRecorder = this.startMediaRecorder.bind(this);
    this.stopMediaRecorder = this.stopMediaRecorder.bind(this);
    this.sendData = this.sendData.bind(this);
  }

  openMediaRecorder() {
    return navigator.mediaDevices.getUserMedia(this.constraintObj)
      .then((mediaStreamObj) => {
        //add listeners for saving video/audio
        this.chunks = [];

        this.mediaRecorder = new MediaRecorder(mediaStreamObj);
        
        this.mediaRecorder.ondataavailable = (ev) => {
          this.chunks.push(ev.data);
        }
        this.mediaRecorder.onstop = (ev) =>{
          var blob = new Blob(this.chunks, {
            type: "audio/wav"
          });
          this.sendData(blob);

          this.chunks = [];
          let audioUrl = window.URL.createObjectURL(blob);
          if (this.audioSave) {
            this.audioSave.src = audioUrl;
          } else {
            this.audioSave = document.getElementById('audio2');
            this.audioSave.src = audioUrl;
          }
          mediaStreamObj.getTracks().forEach(function(track) {
              if (track.readyState == 'live') {
                  track.stop();
              }
          });
          this.mediaRecorder = null;
        }
        
        return Promise.resolve();
      })
      .catch(function(err) { 
        console.log(err);
        return Promise.reject(err);
      });
  }

  sendData(blob) {
    let csrftoken = getCookie('csrftoken');

    let formData = new FormData();
    formData.append('audio_file', blob, 'audio.webm');
    
    fetch('/api/audio', {
      method: 'POST',
      headers: { 
        'X-CSRFToken': csrftoken,
      },
      body: formData
    })
    .then((response => response.json()))
    .then((data) => {
      this.props.updateParent()
    })
    .catch(error => {
      console.log(error);
    });
  }

  startMediaRecorder() {
    if (this.state.isActive === true)
      return;

    
    this.setState({
      isActive: true,
    })
    if (this.mediaRecorder === null) {
      this.openMediaRecorder()
        .then(() =>{
          this.mediaRecorder.start();    
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      this.mediaRecorder.start();
    }
  }


  stopMediaRecorder() {
    if (this.mediaRecorder === null || this.state.isActive === false)
      return;

    this.setState({
      isActive: false,
    })
    this.mediaRecorder.stop();
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
          <audio id="audio2" controls></audio>
      </div>
    );
  }
}
  
