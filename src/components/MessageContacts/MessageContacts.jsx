import "./messageContacts.css";

// images
import onlineFriendImg from "../../images/Frame 76.png";

export default function MessageContacts() {
  return (
    <div className="message-contacts mt-md">
      <div className="message-contacts-header">
        {" "}
        <p className="text-body">Message Contacts</p>
      </div>
      <div className="message-contact-online-friends">
        <ul className="message-contact-online-friends-list mt-sm">
          <li>
            <div className="online-friend-profile-img">
              <img src={onlineFriendImg} alt="" />
            </div>
            <p>Friend Name</p>
          </li>
          <li>
            <div className="online-friend-profile-img">
              <img src={onlineFriendImg} alt="" />
            </div>
            <p>Friend Name</p>
          </li>
          <li>
            <div className="online-friend-profile-img">
              <img src={onlineFriendImg} alt="" />
            </div>
            <p>Friend Name</p>
          </li>
          <li>
            <div className="online-friend-profile-img">
              <img src={onlineFriendImg} alt="" />
            </div>
            <p>Friend Name</p>
          </li>
          <li>
            <div className="online-friend-profile-img">
              <img src={onlineFriendImg} alt="" />
            </div>
            <p>Friend Name</p>
          </li>
        </ul>
      </div>
      <div className="view-all-online-friend">
        <a href="#" className="text-body">
          View All
        </a>
      </div>
    </div>
  );
}
