import "./post.css";

// icons
import { AiFillHeart } from "react-icons/ai";
import { FaRegComment } from "react-icons/fa";
import { BiRepost } from "react-icons/bi";

// images
import posterImg from "../../images/Frame 43.png";
import postImg from "../../images/man-walking-dog.png";

export default function Post() {
  return (
    <div className="postDiv">
      <div className="post">
        <div className="post-head">
          <div className="poster-image">
            <img src={posterImg} alt="" />
          </div>
          <div className="poster-name">
            <h3 className="h-100">Olu of Warri</h3>
          </div>
        </div>
        <div className="post-img">
          <img src={postImg} alt="" />
        </div>
        <div className="post-desc">
          <p className="text-body">
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Deleniti
            dolore ipsa iusto non cupiditate cum id vel dolor dicta tempora?
          </p>
        </div>
        <div className="post-action">
          <div className="post-like-comment">
            <div className="post-like-comment-btn">
              <AiFillHeart className="post-like-icon" />
              <p className="text-body">234</p>
            </div>

            <div className="post-like-comment-btn">
              <FaRegComment className="post-like-icon" />
              <p className="text-body">24</p>
            </div>
          </div>

          <div className="post-repost">
            <p className="text-body">3</p>
            <BiRepost className="post-like-icon" />
          </div>
        </div>

        <div className="post-comments">
          <ul className="post-comments-list">
            <li className="post-comment">
              <div className="commenter-image">
                <img src={posterImg} alt="" />
              </div>
              <p className="text-body comment">
                Lorem ipsum dolor sit amet consectetur adipisicing elit.
                Laboriosam explicabo id tenetur, expedita.
              </p>
            </li>

            <li className="post-comment">
              <div className="commenter-image">
                <img src={posterImg} alt="" />
              </div>
              <p className="text-body comment">
                Lorem ipsum dolor sit amet consectetur adipisicing elit.
                Laboriosam explicabo id tenetur.
              </p>
            </li>
          </ul>
        </div>

        <div className="post-comment-box">
          <div className="user-image">
            <img src={posterImg} alt="" />
          </div>
          <div className="comment-box">
            <input type="text" placeholder="Write your comment..." />
            <button className="btn-solid">Post Comment</button>
          </div>
        </div>
      </div>
    </div>
  );
}
