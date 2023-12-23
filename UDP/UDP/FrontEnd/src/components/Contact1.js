import React, { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import contactImg from "../assets/img/contact-img.svg";
import 'animate.css';
import TrackVisibility from 'react-on-screen';

export const Contact1 = () => {
  const formInitialDetails = {
    password: '',
    file_name: '',
    room_cap: '',
    flag: 1,
  };
  const [formDetails, setFormDetails] = useState(formInitialDetails);
  const [buttonText, setButtonText] = useState('Send');
  const [status, setStatus] = useState({});

  const onFormUpdate = (category, value) => {
    setFormDetails({
      ...formDetails,
      [category]: value,
    });
  };

  const handleFileChange = (e) => {
    const fileName = e.target.files[0] ? e.target.files[0].name : '';
    onFormUpdate('file_name', fileName);
    console.log(fileName);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setButtonText("Sending...");

    try {
      const temp = {
        'file_name': formDetails.file_name,
        'flag': formDetails.flag,
        'password': formDetails.password,
        'room_cap': parseInt(formDetails.room_cap),
      };

      let response = await fetch("http://0.0.0.0:8000/middleware", {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=utf-8",
        },
        body: JSON.stringify(temp),
      });

      if (response.status === 200) {
        let result = await response.json();
        setStatus({ success: true, message: 'Data sent successfully', data: result });
        window.alert(`Response Data; ${JSON.stringify(result)}`);
      } else {
        setStatus({ success: false, message: 'Something went wrong, please try again later.' });
      }
    } catch (error) {
      console.error(error);
      setStatus({ success: false, message: 'Something went wrong, please try again later.' });
    } finally {
      setButtonText("Sent");
    }
  };

  return (
    <section className="contact" id="connect">
      <Container>
        <Row className="align-items-center">
          <Col size={12} md={6}>
            <TrackVisibility>
              {({ isVisible }) => (
                <img className={isVisible ? "animate__animated animate__zoomIn" : ""} src={contactImg} alt="Contact Us" />
              )}
            </TrackVisibility>
          </Col>
          <Col size={12} md={6}>
            <TrackVisibility>
              {({ isVisible }) => (
                <div className={isVisible ? "animate__animated animate__fadeIn" : ""}>
                  <h2>Create New Room</h2>
                  <form onSubmit={handleSubmit}>
                    <Row>
                      <Col size={12} sm={6} className="px-1">
                        <input type="text" value={formDetails.password} placeholder="Enter Room Name" onChange={(e) => onFormUpdate('password', e.target.value)} />
                      </Col>
                      <Col size={12} sm={6} className="px-1">
                        <input type="file" name="file" onChange={handleFileChange} />
                      </Col>
                      <Col size={12} sm={6} className="px-1">
                        <input type="text" value={formDetails.room_cap} placeholder="Enter Room Capacity" onChange={(e) => onFormUpdate('room_cap', e.target.value)} />
                      </Col>
                      <Col size={12} className="px-1" style={{ marginLeft: "190px" }}>
                        <button type="submit"><span>{buttonText}</span></button>
                      </Col>
                      {status.message && (
                        <Col>
                          <p className={status.success === false ? "danger" : "success"}>{status.message}</p>
                        </Col>
                      )}
                    </Row>
                  </form>
                </div>
              )}
            </TrackVisibility>
          </Col>
        </Row>
      </Container>
    </section>
  );
};
