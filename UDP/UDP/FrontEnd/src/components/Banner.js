import { useState, useEffect } from "react";
import { Container, Row, Col } from "react-bootstrap";
import headerImg from "../assets/img/floating_pic.png";
import { ArrowRightCircle } from 'react-bootstrap-icons';
import 'animate.css';
import { Link } from "react-router-dom";
import TrackVisibility from 'react-on-screen';

export const Banner = () => {
  const [activeLink, setActiveLink] = useState('home');
  const [loopNum, setLoopNum] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const [text, setText] = useState('');
  const [delta, setDelta] = useState(100);
  const [index, setIndex] = useState(1);
  const toRotate = [ "Durable.Reliable.Fast." ];
  const period = 3000;

  useEffect(() => {
    let ticker = setInterval(() => {
      tick();
    }, delta);

    return () => { clearInterval(ticker) };
  }, [text])

  const tick = () => {
    let i = loopNum % toRotate.length;
    let fullText = toRotate[i];
    let updatedText = fullText.substring(0, text.length + 1);
    setText(updatedText);
  }
  const onUpdateActiveLink = (value) => {
    setActiveLink(value);
  }

  return (
    <section className="banner" id="home">
      <Container>
        <Row className="aligh-items-center">
          <Col xs={12} md={6} xl={7}>
            <TrackVisibility>
              {({ isVisible }) =>
              <div className={isVisible ? "animate__animated animate__fadeIn" : ""}>
                <h1>{``} <span className="txt-rotate" dataPeriod="1000" data-rotate='[ "Optimizing Your Talent Database Intelligently" ]'><span className="wrap">{text}</span></span></h1>
                <br/><br/>
                  <h4>Transfer Data between your peers blazingly fast using the UDP protocol without losing the data!</h4>
              </div>}
            </TrackVisibility>
          </Col>
          <Col xs={12} md={6} xl={5}>
            <TrackVisibility>
              {({ isVisible }) =>
                <div className={isVisible ? "animate__animated animate__zoomIn" : ""}>
                  <img src={headerImg} alt="Header Img"/>
                </div>}
            </TrackVisibility>
          </Col>
        </Row>
      </Container>
    </section>
  )
}
