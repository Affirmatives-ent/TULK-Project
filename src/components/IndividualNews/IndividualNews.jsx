import "./IndividualNews.css";

// utils
import { Link } from "react-router-dom";

// images
import newsreelImg from "../../images/Frame 40.png";
import commenterImg from "../../images/image-25.png";

// icons
import { AiFillHeart, AiOutlineSend } from "react-icons/ai";
import { FaRegComment } from "react-icons/fa";
import { RiShareBoxFill } from "react-icons/ri";
import { useState } from "react";

export default function IndividualNews({ loginPage, newsItem }) {
  const [newsOpen, setNewsOpen] = useState(false);

  const toggleNewsOpen = () => {
    setNewsOpen(!newsOpen);
  };

  const newsReelclass = newsOpen ? "newsreel active" : "newsreel";
  return (
    <div className={newsReelclass}>
      <div className="newsreel-content" onClick={toggleNewsOpen}>
        <div className="newsreelImg">
          <img src={newsreelImg} alt="" />
        </div>
        <div className="newsreelHead">
          <p className="small-text">{newsItem.newsTag}</p>
          <div className="newsreelHead-header-text">
            <h3 className="h-100">{newsItem.newsHeader}</h3>
          </div>
          {loginPage && (
            <p>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Error
              facere praesentium, cupiditate ad ab ut cumque ea quis. Distinctio
              voluptates doloribus optio maiores omnis eaque suscipit,
              accusantium laboriosam.
            </p>
          )}
        </div>
      </div>
      {newsOpen && (
        <>
          <div className="newsreel-body">
            <p className="text-body">{newsItem.newsBody}</p>
          </div>
          <div className="newsreel-extra">
            <div className="newsreel-time">
              <p className="small-text">{newsItem.newsPostTime}</p>
            </div>
            <div className="newsreel-action">
              <div className="newsreel-like-count">
                <AiFillHeart /> 56
              </div>
              <div className="newsreel-comment-count">
                <FaRegComment /> 26
              </div>
              <div className="newsreel-share">
                <RiShareBoxFill />
              </div>
            </div>
          </div>
          <div className="newsreel-comment-section">
            <div className="commenter-image">
              <img src={commenterImg} alt="" />
            </div>
            <div className="comment-box">
              <input type="text" placeholder="Write your comment..." />
              <button>
                <AiOutlineSend />
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
