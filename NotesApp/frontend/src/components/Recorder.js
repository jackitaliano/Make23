import { useReactMediaRecorder } from "react-media-recorder";
import React, { useEffect, useState } from "react";
import { Button } from '@mui/material';

const Recorder = (props) => {
  const [second, setSecond] = useState("00");
  const [minute, setMinute] = useState("00");
  const [isActive, setIsActive] = useState(false);
  const [counter, setCounter] = useState(0);
  useEffect(() => {
    let intervalId;

    if (isActive) {
      intervalId = setInterval(() => {
        const secondCounter = counter % 60;
        const minuteCounter = Math.floor(counter / 60);

        let computedSecond =
          String(secondCounter).length === 1
            ? `0${secondCounter}`
            : secondCounter;
        let computedMinute =
          String(minuteCounter).length === 1
            ? `0${minuteCounter}`
            : minuteCounter;

        setSecond(computedSecond);
        setMinute(computedMinute);

        setCounter((counter) => counter + 1);
      }, 1000);
    }

    return () => clearInterval(intervalId);
  }, [isActive, counter]);

  function stopTimer() {
    setIsActive(false);
    setCounter(0);
    setSecond("00");
    setMinute("00");
  }
  const {
    status,
    startRecording,
    stopRecording,
    pauseRecording,
    mediaBlobUrl
  } = useReactMediaRecorder({
    video: false,
    audio: true,
    echoCancellation: true
  });

  return (
    <div>
        <Button
        color="success"
        variant={isActive ? "outlined" : "contained"} 
        onClick={() => {
            if (!isActive) {
            startRecording();
            } else {
            pauseRecording();
            }

            setIsActive(!isActive);
        }}
        >
        {isActive ? "Pause" : "Start"}
        </Button>
        <Button
        color="error"
        variant="contained" 
        onClick={() => {
            pauseRecording();
            stopRecording();

            setIsActive(false);
        }}
        >
        Stop
        </Button>
    </div>
  );
};
export default Recorder;
