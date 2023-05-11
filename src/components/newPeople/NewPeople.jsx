import "./newPeople.css";

// images
import newPerson1 from "../../images/Frame 76.png";
import newPerson2 from "../../images/Frame 85.png";
import newPerson3 from "../../images/Frame 86.png";

export default function NewPeople() {
  return (
    <div className="newPeopleDiv mt-md">
      <div className="newPeopleHeader">
        <p className="text-body">Who is new</p>
      </div>
      <div className="newPeople">
        <div className="newPerson">
          <img src={newPerson2} alt="" />
        </div>
        <div className="newPerson">
          <img src={newPerson1} alt="" />
        </div>
        <div className="newPerson">
          <img src={newPerson3} alt="" />
        </div>
      </div>
      <div className="load-more-new-people">
        <a href="#" className="text-body">
          More
        </a>
      </div>
    </div>
  );
}
