import React from "react";

// styles
import "./notifications.css";

// icons
import { IoIosClose } from "react-icons/io";
import notifBell from "../../images/icons/notif-bell.png";

// images
import notifImg1 from "../../images/Frame 91.png";
import notifImg2 from "../../images/Frame 76.png";
import notifImg3 from "../../images/Frame 84.png";
import notifImg4 from "../../images/Frame 85.png";
import notifImg5 from "../../images/Frame 86.png";

export default function Notifications({ desktop, setNotificationOpen }) {
  return (
    <div className="notifications">
      <div className="notifications-header">
        <h3 className="h-100">Notifications</h3>
        {/* show bell in header on mobile */}
        {!desktop && <img src={notifBell} alt="" />}

        {desktop && (
          <div
            className="notification-close-btn"
            id="notificationCloseBtn"
            onClick={() => setNotificationOpen(false)}
          >
            <IoIosClose />
          </div>
        )}
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg1} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Funmi Wilson</b> wants to be your friend
          </p>
          <div className="notification-action-btns">
            <button className="accept">Accept</button>
            <button className="reject">Reject</button>
          </div>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg2} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Kingsley Benjamin</b> and 36 other friends are celebrating
            birthday today
          </p>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg3} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Ayo Silas</b> and 52 others commented on your post
          </p>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg4} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Olu of Warri</b> invited you to join <b>Great Warri Reunion </b>
            group
          </p>
          <div className="notification-action-btns">
            <button className="accept">Accept</button>
            <button className="reject">Reject</button>
          </div>
        </div>
      </div>
      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg5} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Faith Oham</b> and 17 others shared your post
          </p>
        </div>
      </div>
      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg1} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Funmi Wilson</b> wants to be your friend
          </p>
          <div className="notification-action-btns">
            <button className="accept">Accept</button>
            <button className="reject">Reject</button>
          </div>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg2} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Kingsley Benjamin</b> and 36 other friends are celebrating
            birthday today
          </p>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg3} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Ayo Silas</b> and 52 others commented on your post
          </p>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg4} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Olu of Warri</b> invited you to join <b>Great Warri Reunion </b>
            group
          </p>
          <div className="notification-action-btns">
            <button className="accept">Accept</button>
            <button className="reject">Reject</button>
          </div>
        </div>
      </div>
      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg5} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Faith Oham</b> and 17 others shared your post
          </p>
        </div>
      </div>
      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg1} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Funmi Wilson</b> wants to be your friend
          </p>
          <div className="notification-action-btns">
            <button className="accept">Accept</button>
            <button className="reject">Reject</button>
          </div>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg2} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Kingsley Benjamin</b> and 36 other friends are celebrating
            birthday today
          </p>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg3} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Ayo Silas</b> and 52 others commented on your post
          </p>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg4} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Olu of Warri</b> invited you to join <b>Great Warri Reunion </b>
            group
          </p>
          <div className="notification-action-btns">
            <button className="accept">Accept</button>
            <button className="reject">Reject</button>
          </div>
        </div>
      </div>
      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg5} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Faith Oham</b> and 17 others shared your post
          </p>
        </div>
      </div>
      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg1} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Funmi Wilson</b> wants to be your friend
          </p>
          <div className="notification-action-btns">
            <button className="accept">Accept</button>
            <button className="reject">Reject</button>
          </div>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg2} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Kingsley Benjamin</b> and 36 other friends are celebrating
            birthday today
          </p>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg3} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Ayo Silas</b> and 52 others commented on your post
          </p>
        </div>
      </div>

      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg4} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Olu of Warri</b> invited you to join <b>Great Warri Reunion </b>
            group
          </p>
          <div className="notification-action-btns">
            <button className="accept">Accept</button>
            <button className="reject">Reject</button>
          </div>
        </div>
      </div>
      <div className="notification">
        <div className="notification-user-image">
          <img src={notifImg5} alt="" />
        </div>
        <div className="notification-content">
          <p className="text-body">
            <b>Faith Oham</b> and 17 others shared your post
          </p>
        </div>
      </div>
    </div>
  );
}
