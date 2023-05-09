import "./groups.css";

// images
import newPerson1 from "../../images/Frame 76.png";
import newPerson2 from "../../images/Frame 85.png";
import newPerson3 from "../../images/Frame 86.png";

export default function Groups() {
  return (
    <div className="groupsDiv mt-md">
      <div className="groups-header">
        <p className="text-body">My Groups</p>
      </div>

      <div className="groups">
        <div className="group">
          <img src={newPerson2} alt="" />
        </div>
        <div className="group">
          <img src={newPerson1} alt="" />
        </div>
        <div className="group">
          <img src={newPerson3} alt="" />
        </div>
      </div>
      <div className="load-more-groups">
        <a href="#" className="text-body mt-xsm">
          View All
        </a>
      </div>
    </div>
  );
}
