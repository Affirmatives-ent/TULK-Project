// styles
import "./newsreel.css";

// components
import IndividualNews from "../IndividualNews/IndividualNews";

// data
import { news } from "../../data/data";

export default function Newsreel({ loginPage }) {
  return (
    <div className="newsreelDiv">
      {news.map((newsItem) => {
        return (
          <IndividualNews
            key={newsItem.newsId}
            newsItem={newsItem}
            loginPage={loginPage}
          />
        );
      })}
    </div>
  );
}
