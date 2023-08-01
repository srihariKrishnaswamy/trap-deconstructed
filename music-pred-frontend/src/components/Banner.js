import React from 'react';
import Container from "react-bootstrap/Container";
import classes from "./Banner.module.css";

function Banner() {
  return (
    <Container className={classes.nav}>
        <a href="/" className={classes.site_title}>Trap Deconstructed</a>
        <ul>
            <li>
                <a href="/about" className={classes.about}>About</a>
            </li>
        </ul>
    </Container>
  )
}

export default Banner