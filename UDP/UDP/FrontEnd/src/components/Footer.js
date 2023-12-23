import { Container, Row, Col } from "react-bootstrap";
import logo from "../assets/img/iiit_logo.png";
import navIcon1 from "../assets/img/nav-icon1.svg";
import navIcon2 from "../assets/img/nav-icon2.svg";
import navIcon3 from "../assets/img/nav-icon3.svg";

export const Footer = () => {
  return (
    <footer className="footer" id ="footer">
      <Container>
          <br/><br/>
          <Row>
            <h1>About Us</h1>
            <br/><br/><br/>
          <h5>We are Innovative tech company specializing in AI and data solutions that mpowers businesses with smart insights and automation and drives growth and efficiency through cutting-edge technology.</h5>
          </Row>
          <br/><br/><br/>
        <Row className="align-items-center">
          <Col size={12} sm={6}>
            <img src={logo} alt="Logo" />
          </Col>
          <Col size={12} sm={6} className="text-center text-sm-end">
            <br/><br/><br/><br/>
            <div className="social-icon">
              <a href="https://www.linkedin.com/company/ihub-data/?originalSubdomain=in"><img src={navIcon1} alt="Icon" /></a>
            </div>
            <p>Copyright-Ilomilo 2023. All Rights Reserved</p>
          </Col>
        </Row>
      </Container>
    </footer>
  )
}
