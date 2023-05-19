// styles
import "./news.css";

// images
import newsImg from "../../images/Frame 45.png";

// icons
import { AiFillHeart } from "react-icons/ai";
import { FaRegComment } from "react-icons/fa";
import { BiRepost } from "react-icons/bi";
import { RiShareBoxFill } from "react-icons/ri";

export default function News({ loginPage, newsPage }) {
  return (
    <div className="newsDiv">
      <div className="news">
        <div className="news-content">
          <div className="newsImg">
            <img src={newsImg} alt="" />
          </div>
          <div className="newsBody">
            {newsPage && <p className="small-text">Politics</p>}
            <div className="newsBody-header-text">
              <h3 className="h-100">
                Obasanjo faults appointment of former IGPs as chairmen
              </h3>
            </div>
            {loginPage && (
              <p>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Error
                facere praesentium, cupiditate ad ab ut cumque ea quis.
                Distinctio voluptates doloribus optio maiores omnis eaque
                suscipit, accusantium laboriosam.
              </p>
            )}
          </div>
        </div>
        {newsPage && (
          <div className="news-extra">
            <div className="news-time">
              <p className="small-text">15 mins ago</p>
            </div>
            <div className="news-action">
              <div className="news-like-count">
                <AiFillHeart /> 56
              </div>
              <div className="news-comment-count">
                <FaRegComment /> 26
              </div>
              <div className="news-share">
                <RiShareBoxFill />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="news">
        <div className="news-content">
          <div className="newsImg">
            <img src={newsImg} alt="" />
          </div>
          <div className="newsBody">
            {newsPage && <p className="small-text">Politics</p>}
            <div className="newsBody-header-text">
              <h3 className="h-100">
                Obasanjo faults appointment of former IGPs as chairmen
              </h3>
            </div>
            {loginPage && (
              <p>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Error
                facere praesentium, cupiditate ad ab ut cumque ea quis.
                Distinctio voluptates doloribus optio maiores omnis eaque
                suscipit, accusantium laboriosam.
              </p>
            )}
          </div>
        </div>
        {newsPage && (
          <div className="news-extra">
            <div className="news-time">
              <p className="small-text">15 mins ago</p>
            </div>
            <div className="news-action">
              <div className="news-like-count">
                <AiFillHeart /> 56
              </div>
              <div className="news-comment-count">
                <FaRegComment /> 26
              </div>
              <div className="news-share">
                <RiShareBoxFill />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="news">
        <div className="news-content">
          <div className="newsImg">
            <img src={newsImg} alt="" />
          </div>
          <div className="newsBody">
            {newsPage && <p className="small-text">Politics</p>}
            <div className="newsBody-header-text">
              <h3 className="h-100">
                Obasanjo faults appointment of former IGPs as chairmen
              </h3>
            </div>
            {loginPage && (
              <p>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Error
                facere praesentium, cupiditate ad ab ut cumque ea quis.
                Distinctio voluptates doloribus optio maiores omnis eaque
                suscipit, accusantium laboriosam.
              </p>
            )}
          </div>
        </div>
        {newsPage && (
          <div className="news-extra">
            <div className="news-time">
              <p className="small-text">15 mins ago</p>
            </div>
            <div className="news-action">
              <div className="news-like-count">
                <AiFillHeart /> 56
              </div>
              <div className="news-comment-count">
                <FaRegComment /> 26
              </div>
              <div className="news-share">
                <RiShareBoxFill />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="news">
        <div className="news-content">
          <div className="newsImg">
            <img src={newsImg} alt="" />
          </div>
          <div className="newsBody">
            {newsPage && <p className="small-text">Politics</p>}
            <div className="newsBody-header-text">
              <h3 className="h-100">
                Obasanjo faults appointment of former IGPs as chairmen
              </h3>
            </div>
            {loginPage && (
              <p>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Error
                facere praesentium, cupiditate ad ab ut cumque ea quis.
                Distinctio voluptates doloribus optio maiores omnis eaque
                suscipit, accusantium laboriosam.
              </p>
            )}
          </div>
        </div>
        {newsPage && (
          <div className="news-extra">
            <div className="news-time">
              <p className="small-text">15 mins ago</p>
            </div>
            <div className="news-action">
              <div className="news-like-count">
                <AiFillHeart /> 56
              </div>
              <div className="news-comment-count">
                <FaRegComment /> 26
              </div>
              <div className="news-share">
                <RiShareBoxFill />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="news">
        <div className="news-content">
          <div className="newsImg">
            <img src={newsImg} alt="" />
          </div>
          <div className="newsBody">
            {newsPage && <p className="small-text">Politics</p>}
            <div className="newsBody-header-text">
              <h3 className="h-100">
                Obasanjo faults appointment of former IGPs as chairmen
              </h3>
            </div>
            {loginPage && (
              <p>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Error
                facere praesentium, cupiditate ad ab ut cumque ea quis.
                Distinctio voluptates doloribus optio maiores omnis eaque
                suscipit, accusantium laboriosam.
              </p>
            )}
          </div>
        </div>
        {newsPage && (
          <div className="news-extra">
            <div className="news-time">
              <p className="small-text">15 mins ago</p>
            </div>
            <div className="news-action">
              <div className="news-like-count">
                <AiFillHeart /> 56
              </div>
              <div className="news-comment-count">
                <FaRegComment /> 26
              </div>
              <div className="news-share">
                <RiShareBoxFill />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="news">
        <div className="news-content">
          <div className="newsImg">
            <img src={newsImg} alt="" />
          </div>
          <div className="newsBody">
            {newsPage && <p className="small-text">Politics</p>}
            <div className="newsBody-header-text">
              <h3 className="h-100">
                Obasanjo faults appointment of former IGPs as chairmen
              </h3>
            </div>
            {loginPage && (
              <p>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Error
                facere praesentium, cupiditate ad ab ut cumque ea quis.
                Distinctio voluptates doloribus optio maiores omnis eaque
                suscipit, accusantium laboriosam.
              </p>
            )}
          </div>
        </div>
        {newsPage && (
          <div className="news-extra">
            <div className="news-time">
              <p className="small-text">15 mins ago</p>
            </div>
            <div className="news-action">
              <div className="news-like-count">
                <AiFillHeart /> 56
              </div>
              <div className="news-comment-count">
                <FaRegComment /> 26
              </div>
              <div className="news-share">
                <RiShareBoxFill />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="news">
        <div className="news-content">
          <div className="newsImg">
            <img src={newsImg} alt="" />
          </div>
          <div className="newsBody">
            {newsPage && <p className="small-text">Politics</p>}
            <div className="newsBody-header-text">
              <h3 className="h-100">
                Obasanjo faults appointment of former IGPs as chairmen
              </h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
