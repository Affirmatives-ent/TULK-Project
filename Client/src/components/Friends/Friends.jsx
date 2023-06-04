import React from "react";

// styles
import "./friends.css";

// images
import newPerson1 from "../../images/Frame 76.png";
import newPerson2 from "../../images/Frame 85.png";
import newPerson3 from "../../images/Frame 86.png";

export default function Friends() {
  return (
    <div className="friendsDiv mt-lg">
      <div className="friends-header">
        <h3 className="h-100">My Friends</h3>
        <div className="load-more-friends">
          <a href="#" className="text-body mt-xsm">
            View All
          </a>
        </div>
      </div>

      <div className="friends">
        <div className="friend">
          <img src={newPerson2} alt="" />
        </div>
        <div className="friend">
          <img src={newPerson1} alt="" />
        </div>
        <div className="friend">
          <img src={newPerson3} alt="" />
        </div>

        <div className="friend">
          <img src={newPerson2} alt="" />
        </div>
        <div className="friend">
          <img src={newPerson1} alt="" />
        </div>
        <div className="friend">
          <img src={newPerson3} alt="" />
        </div>
      </div>
    </div>
  );
}
