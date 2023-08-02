import React, { useState, useEffect } from 'react';
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import classes from "./MainSection.module.css";
import appClasses from "../App.module.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMicrophone } from '@fortawesome/free-solid-svg-icons';
import recbutton from '../images/recbutton.png';
import AudioRecorder from './AudioRecorder'

function MainSection() {
  const [showRecording, setShowRecording] = useState(false);
  const [recordingProcessing, setRecordingProcessing] = useState(false);
  const [isDisabled, setIsDisabled] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const toggleShowRecording = (boolVal) => {
    setShowRecording(boolVal);
  };

  const toggleRecProcessing = (boolVal) => {
    setRecordingProcessing(boolVal);
  }

  useEffect(() => {
    console.log('RE-RENDERING POTENT')
    if (showRecording || recordingProcessing) {
      setIsDisabled(true);
    } else {
      setIsDisabled(false);
    }
  }, [showRecording, recordingProcessing])

  useEffect(() => {
    console.log('PARENT COMP LOADED')
  }, [])

  return (
    <section className={appClasses.mainsection}>
        <Container className={classes.container}>
            <Col xs={7} className={classes.heading}>
              <h1 className={classes.bigtext}>Play a trap song</h1>
            </Col>
            <Col>
            <button onClick={() => {setShowResults(false); toggleShowRecording(true)}} disabled={isDisabled} className={`${classes.circularbutton} ${classes.circularbutton}`}>
              <div className={classes.micboundary}>
              <FontAwesomeIcon icon={faMicrophone} className={classes.icon} size="10x" style={{ color: 'rgb(255, 0, 0)' }} />
              </div>
            </button>
            </Col>
            <Col>
              {showRecording && <RecordingPanel recProcessing={toggleRecProcessing} showRecording={toggleShowRecording}/>}
              {(recordingProcessing || showResults) && <RecordingProcessing recProcessing={toggleRecProcessing} setShowResults={setShowResults} fetched={showResults}/>}
            </Col>  
        </Container>
    </section>
  )
}

function RecordingProcessing({recProcessing, setShowResults, fetched}) {
  const [data, setData] = useState([{}])
  const [tempo, setTempo] = useState("")
  const [feel, setFeel] = useState("")
  const [key, setKey] = useState("")
  const [mode, setMode] = useState("")
  const [messages, setMessages] = useState([])

  const parseResults = (unparsed) => { // tempo feel key mode message
    if (unparsed) {
      var numPipes = 0;
      var tempoSmall = "";
      var feelSmall = "";
      var keySmall = "";
      var modeSmall = "";
      var currMsg = "";
      var messagesSmall = [];
      for (let i = 0; i < unparsed.length; i++) {
        if (unparsed[i] === '|') {
          numPipes +=1;
        } else if (numPipes === 0) {
          tempoSmall += unparsed[i];
        } else if (numPipes === 1) {
          feelSmall += unparsed[i];
        } else if (numPipes === 2) {
          keySmall += unparsed[i];
        } else if (numPipes === 3) {
          modeSmall += unparsed[i];
        } else if (numPipes === 4) {
          if (unparsed[i] === "\n") {
            messagesSmall.push(currMsg);
            currMsg = "";
          } else {
            currMsg += unparsed[i];
          }
        }
      }
      // console.log(`tempo: ${tempoSmall}`);
      // console.log(`feel: ${feelSmall}`);
      // console.log(`key: ${keySmall}`);
      // console.log(`mode: ${modeSmall}`)
      // console.log(`messages: ${messagesSmall}`)
      if (localStorage.getItem('tempo') && localStorage.getItem('feel') && localStorage.getItem('key') && localStorage.getItem('mode') && localStorage.getItem('messages')) {
        if (!(JSON.parse(localStorage.getItem('tempo')) === tempoSmall && JSON.parse(localStorage.getItem('feel')) === feelSmall && JSON.parse(localStorage.getItem('key')) === keySmall && JSON.parse(localStorage.getItem('mode')) === modeSmall)) {
          setTempo(tempoSmall);
          setFeel(feelSmall);
          setKey(keySmall);
          setMode(modeSmall);
          setMessages(messagesSmall);
          localStorage.setItem('tempo', JSON.stringify(tempoSmall));
          localStorage.setItem('feel', JSON.stringify(feelSmall));
          localStorage.setItem('key', JSON.stringify(keySmall));
          localStorage.setItem('mode', JSON.stringify(modeSmall));
          localStorage.setItem('messages', JSON.stringify(messagesSmall));
        } else {
          setTempo(tempoSmall);
          setFeel(feelSmall);
          setKey(keySmall);
          setMode(modeSmall);
          setMessages(JSON.parse(localStorage.getItem('messages')));
        }
      } else {
        setTempo(tempoSmall);
        setFeel(feelSmall);
        setKey(keySmall);
        setMode(modeSmall);
        setMessages(messagesSmall);
        localStorage.setItem('tempo', JSON.stringify(tempoSmall));
        localStorage.setItem('feel', JSON.stringify(feelSmall));
        localStorage.setItem('key', JSON.stringify(keySmall));
        localStorage.setItem('mode', JSON.stringify(modeSmall));
        localStorage.setItem('messages', JSON.stringify(messagesSmall));
      }
    }
  }

  useEffect(() => {
    // console.log('THIS COMPONENT IS LOADED')
    if (!fetched && tempo === "") {
      console.log('SUPPOSED TO FETCH (INSIDE REACT APP)')
      fetch("/get_results").then(
        res => res.json()
      ).then(
        newData => {
          console.log('FETCHED INSIDE REACT APP')
          setData(newData)
          parseResults(newData.stdout)
          console.log(`the data: ${newData.stdout}`)
          setShowResults(true);
          recProcessing(false);
        }
      )
    }
  }, [])
  return (
    <section>
      {!fetched ? (
        <p className={classes.waitingfordata}>Processing...</p>
      ): (
        <Container className={classes.displaycontainer}>
            <Col>
              <Row>
                <div className={classes.displaycol}>
                  <h2 className={classes.waitingfordata}>The sample is at <b>{tempo}</b> bpm in the key of <b>{key} {mode}</b> and feels <b>{feel}.</b></h2>
                </div>
              </Row>
              <Row>
                <div className={classes.blackdisplayrow}>
                  <div className={classes.internalblackdisp}>
                    <h3 className={classes.waitingfordata}>Tips to create a similar vibe:</h3>
                    <div className={classes.suggestions}>
                      <p className={classes.detailstext}>{messages[0]}</p>
                      <p className={classes.detailstext}>{messages[1]}</p>
                      <p className={classes.detailstext}>{messages[2]}</p>
                    </div>
                  </div>
                </div>
              </Row>
            </Col>
        </Container>
      )}
    </section>
  )
}

function RecordingPanel({recProcessing, showRecording}) {
  const [timer, setTimer] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimer((prevTimer) => {
        // Check if the timer has reached 10 seconds
        if (prevTimer === 10) {
          clearInterval(interval); // Stop the interval
          return prevTimer; // Keep the timer value at 10 seconds
        }
        return prevTimer + 1; // Increment the timer value
      });
    }, 1000);

    // Clean up the timer when the component unmounts
    return () => {
      clearInterval(interval);
    };
  }, []); // Empty dependency array to run the effect only once on component mount

  return (
    <section className={classes.recordingsection}>
      <Container className={classes.recpanel}>
        <div className={classes.content}>
          <div className={classes.buttons}>
            <div className={classes.recbuttoncontainer}>
              <img src={recbutton} className={classes.recimage} alt="Recording icon" />
            </div>
            <div className={classes.rectext}>Recording Audio</div>
          </div>
          <div className={classes.timeremaining}>
            Time Remaining: {10 - timer} seconds
          </div>
          <div>
            <AudioRecorder showRecordingFn={showRecording} recProcessingFn={recProcessing}/>
          </div>
        </div>
      </Container>
    </section>
  );
}


export default MainSection