import React from "react";

// styles
import "./chat.css";

// icons
import { VscSmiley } from "react-icons/vsc";
import { MdPermMedia } from "react-icons/md";
import { RiAttachment2 } from "react-icons/ri";
import { IoIosClose } from "react-icons/io";

// images
import chatHeadImg from "../../images/Frame 40.png";

export default function Chat({ setShowChatModal }) {
  // Function to close chat
  const closeChat = () => {
    setShowChatModal(false);
  };
  return (
    <div className="chat-box">
      <div className="chat-head">
        <div className="chat-head-img">
          <img src={chatHeadImg} alt="" />
        </div>
        <h3 className="h-100">Precious Lazarus</h3>
        <div className="chat-close-btn" onClick={closeChat}>
          <IoIosClose />
        </div>
      </div>

      <div className="chat-body">
        <div className="chat-body-messages">
          <div className="chat-body-sent-message">
            <p className="text-body">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Delectus
              nisi eos eveniet laborum nihil. Officia!
            </p>
          </div>
          <div className="chat-body-received-message">
            <p className="text-body">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Delectus
              nisi eos eveniet laborum nihil. Officia!
            </p>
          </div>
          <div className="chat-body-sent-message">
            <p className="text-body">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Delectus
              nisi eos eveniet laborum nihil. Officia!
            </p>
          </div>
          <div className="chat-body-received-message">
            <p className="text-body">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Delectus
              nisi eos eveniet laborum nihil. Officia!
            </p>
          </div>
          <div className="chat-body-sent-message">
            <p className="text-body">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Delectus
              nisi eos eveniet laborum nihil. Officia!
            </p>
          </div>
          <div className="chat-body-received-message">
            <p className="text-body">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Delectus
              nisi eos eveniet laborum nihil. Officia!
            </p>
          </div>
          <div className="chat-body-sent-message">
            <p className="text-body">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Delectus
              nisi eos eveniet laborum nihil. Officia!
            </p>
          </div>
          <div className="chat-body-received-message">
            <p className="text-body">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Delectus
              nisi eos eveniet laborum nihil. Officia!
            </p>
          </div>
        </div>
        <div className="chat-body-text-input">
          <textarea rows="3" placeholder="Write Message..."></textarea>
        </div>
        <div className="chat-body-actions">
          <div className="chat-body-media-input">
            <VscSmiley className="chat-body-icon" />
            <MdPermMedia className="chat-body-icon" />
            <RiAttachment2 className="chat-body-icon" />
          </div>
          <div className="chat-body-send-btn btn-solid">Send</div>
        </div>
      </div>
    </div>
  );
}
