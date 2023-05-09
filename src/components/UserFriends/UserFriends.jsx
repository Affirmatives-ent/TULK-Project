// styles
import "./userFriends.css";

// images
import userPhoto6 from "../../images/Frame 76.png";

export default function UserFriends() {
  return (
    <div className="user-friends-div">
      <div className="user-friends">
        <div className="user-friend">
          <div className="user-friend-image">
            <img src={userPhoto6} alt="" />
          </div>
          <div className="user-friend-name-location">
            <h3 className="h100">Chris Pessi</h3>
            <small className="small-text">Location: Japan</small>
          </div>
        </div>

        <div className="user-friend">
          <div className="user-friend-image">
            <img src={userPhoto6} alt="" />
          </div>
          <div className="user-friend-name-location">
            <h3 className="h100">Chris Pessi</h3>
            <small className="small-text">Location: Japan</small>
          </div>
        </div>

        <div className="user-friend">
          <div className="user-friend-image">
            <img src={userPhoto6} alt="" />
          </div>
          <div className="user-friend-name-location">
            <h3 className="h100">Chris Pessi</h3>
            <small className="small-text">Location: Japan</small>
          </div>
        </div>

        <div className="user-friend">
          <div className="user-friend-image">
            <img src={userPhoto6} alt="" />
          </div>
          <div className="user-friend-name-location">
            <h3 className="h100">Chris Pessi</h3>
            <small className="small-text">Location: Japan</small>
          </div>
        </div>

        <div className="user-friend">
          <div className="user-friend-image">
            <img src={userPhoto6} alt="" />
          </div>
          <div className="user-friend-name-location">
            <h3 className="h100">Chris Pessi</h3>
            <small className="small-text">Location: Japan</small>
          </div>
        </div>

        <div className="user-friend">
          <div className="user-friend-image">
            <img src={userPhoto6} alt="" />
          </div>
          <div className="user-friend-name-location">
            <h3 className="h100">Chris Pessi</h3>
            <small className="small-text">Location: Japan</small>
          </div>
        </div>
      </div>
      <div className="profile-see-all-friends-btn">
        <a href="#">See All</a>
      </div>
    </div>
  );
}
