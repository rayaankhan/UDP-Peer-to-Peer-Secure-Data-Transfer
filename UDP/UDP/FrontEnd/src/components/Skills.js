import meter1 from "../assets/img/meter1.svg";
import meter2 from "../assets/img/meter2.svg";
import meter3 from "../assets/img/meter3.svg";
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import arrow1 from "../assets/img/arrow1.svg";
import arrow2 from "../assets/img/arrow2.svg";
import colorSharp from "../assets/img/color-sharp.png"

export const Skills = () => {
  const responsive = {
    superLargeDesktop: {
      // the naming can be any, depends on you.
      breakpoint: { max: 4000, min: 3000 },
      items: 5
    },
    desktop: {
      breakpoint: { max: 3000, min: 1024 },
      items: 3
    },
    tablet: {
      breakpoint: { max: 1024, min: 464 },
      items: 2
    },
    mobile: {
      breakpoint: { max: 464, min: 0 },
      items: 1
    }
  };

  return (
    <section className="skill" id="skills">
        <div className="container">
            <div className="row">
                <div className="col-12">
                    <div className="skill-bx wow zoomIn">
                        <h2>Understanding MBTI</h2>
                        <h5>The Myers-Briggs Type Indicator (MBTI) is a widely recognized personality assessment tool that provides insights into an individual's psychological preferences and behaviors. Developed by Katharine Cook Briggs and her daughter Isabel Briggs Myers in the mid-20th century, MBTI has become a popular framework for understanding human personality. Here, we delve into the key aspects of MBTI, its history, and its practical applications.

The Four Dichotomies:
MBTI classifies individuals into 16 distinct personality types based on four dichotomies:

Extraversion (E) vs. Introversion (I): This dichotomy assesses how individuals gain energy, either from social interactions (extraversion) or solitude and introspection (introversion).

Sensing (S) vs. Intuition (N): It examines how people perceive information – either through concrete data and sensory experiences (sensing) or through patterns, possibilities, and symbolism (intuition).

Thinking (T) vs. Feeling (F): This dichotomy explores decision-making processes, distinguishing those who prioritize logic and analysis (thinking) from those who emphasize emotions and values (feeling).

Judging (J) vs. Perceiving (P): MBTI looks at how individuals organize their lives and make choices. Judgers prefer structure, planning, and closure, while perceivers value flexibility and adaptability.</h5>
                    </div>
                </div>
            </div>
        </div>
        <img className="background-image-left" src={colorSharp} alt="Image" />
    </section>
  )
}
