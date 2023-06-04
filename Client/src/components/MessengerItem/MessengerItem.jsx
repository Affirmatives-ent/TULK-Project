import React from "react";

// styles
import "./messengerItem.css";

// images
import messengerImg from "../../images/image-25.png";

export default function MessengerItem() {
  return (
    <div className="messenger-item">
      <div className="messenger-item-left">
        <div className="messenger-img">
          <img src={messengerImg} alt="" />
        </div>
        <div className="messenger-item-left-center">
          <div className="messenger-name">
            <h3 className="h-100">Ugor Sanchez Monroe</h3>
            <div className="messenger-last-message">
              <p className="text-body">Lorem ipsum dolor sit amet...</p>
            </div>
          </div>
        </div>
      </div>
      <div className="messenger-item-right">
        <div className="messenger-last-message-time">
          <small className="small-text"> 11:55pm </small>
        </div>
        <div className="messenger-unread-message-count">13</div>
      </div>
    </div>
  );
}
