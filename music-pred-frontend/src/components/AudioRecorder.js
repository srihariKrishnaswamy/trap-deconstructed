import React, { useEffect, useState } from 'react';
import { encode } from 'wav-encoder';
import axios from 'axios';

function AudioRecorder({ showRecordingFn, recProcessingFn }) {
  const [isRecording, setIsRecording] = useState(true);
  const [mediaStream, setMediaStream] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setMediaStream(stream);

      const audioContext = new AudioContext();
      const sourceNode = audioContext.createMediaStreamSource(stream);

      const bufferSize = 4096;
      const recorder = audioContext.createScriptProcessor(bufferSize, 1, 1);

      let recordedChunks = [];
      recorder.onaudioprocess = (event) => {
        recordedChunks.push([...event.inputBuffer.getChannelData(0)]);
      };

      sourceNode.connect(recorder);
      recorder.connect(audioContext.destination);

      // Stop recording after 10 seconds
      setTimeout(() => {
        setIsRecording(false);
        sourceNode.disconnect();
        recorder.disconnect();
        setAudioChunks(recordedChunks);
        stream.getTracks().forEach((track) => track.stop());
      }, 10000);
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const saveAudio = async () => {
    if (audioChunks.length === 0) {
      console.warn('No audio data recorded.');
      return;
    }
    try {
      const audioData = audioChunks.flat();
      const audioBuffer = new AudioContext().createBuffer(
        1,
        audioData.length,
        new AudioContext().sampleRate
      );
      audioBuffer.getChannelData(0).set(audioData);

      const wavData = await encode({
        sampleRate: audioBuffer.sampleRate,
        channelData: [audioBuffer.getChannelData(0)],
      });

      const wavBlob = new Blob([new DataView(wavData)], { type: 'audio/wav' });

      const formData = new FormData();
      formData.append('audio', wavBlob, 'audio.wav');

      await axios.post('/save_audio', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      console.log('Audio saved successfully');
      showRecordingFn(false);
      recProcessingFn(true);
    } catch (error) {
      console.error('Error saving audio:', error);
    }
  };

  useEffect(() => {
    if (isRecording) {
      startRecording();
    } else {
      saveAudio();
    }
  }, [isRecording]);

  return <></>;
}

export default AudioRecorder;