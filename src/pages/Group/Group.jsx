import React from "react";

// styles
import "./group.css";

// images
import profileCoverPhoto from "../../images/flowers-276014__340 1.png";
import profileUserAvatar from "../../images/image-25.png";
import { useState } from "react";
import Post from "../../components/Post/Post";
import CreatePost from "../../components/CreatePost/CreatePost";

// icons
import { BsGear } from "react-icons/bs";
import { AiOutlineUserAdd } from "react-icons/ai";
import { BiDoorOpen } from "react-icons/bi";

// data
import { posts, users } from "../../data/data";

export default function Group() {
  const [showGroupActionLinks, setShowGroupActionLinks] = useState(false);

  // function to toggle group action links visibility
  const toggleGroupActionLinks = () => {
    setShowGroupActionLinks(!showGroupActionLinks);
  };

  return (
    <div className="group-page">
      <div className="group-data">
        <div className="group-cover-photo">
          <img src={profileCoverPhoto} alt="" />
        </div>
        <div className="group-image-name">
          <div className="group-avatar">
            <img src={profileUserAvatar} alt="" />
          </div>
          <div className="group-name-slogan">
            <h2 className="h-200">Friends of Nature</h2>
            <div className="group-slogan mt-xsm">
              <p>Social</p>
              <div className="group-members-count">
                <p>3050 Members</p>
              </div>
            </div>
          </div>

          <div className="group-edit-button">
            <button className="btn-solid">
              <BiDoorOpen className="icon" /> Join
            </button>
            <button className="btn-secondary">
              <AiOutlineUserAdd className="icon" />
              Invite
            </button>
            <button className="btn-secondary">
              <BsGear className="icon" /> Settings
            </button>
          </div>
        </div>
      </div>

      <div className="group-info">
        <h3 className="h-100">
          <b> Slogan: </b> <br />
          Make Friend With Nature and Be Free
        </h3>
        <h3 className="h-100">
          <b>Group introduction message</b> <br />
          Lorem ipsum dolor sit amet consectetur. Turpis porta mi aenean platea.
          Quam eu tellus faucibus amet nibh lobortis. Ac facilisis quis leo est
          et euismod ultricies vulputate viverra. Purus arcu adipiscing turpis
          augue facilisis posuere.
        </h3>
      </div>

      <div className="group-posts">
        <CreatePost />
        {/* <Post userId={users[0].id} /> */}
      </div>
    </div>
  );
}
