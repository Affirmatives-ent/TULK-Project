import React from "react";

// styles
import "./newsreel.css";

// components
import IndividualNews from "../IndividualNews/IndividualNews";

// utils
import { useState, useEffect } from "react";
import axios from "axios";

// icons
import { TfiLayoutGrid3Alt } from "react-icons/tfi";
import { BsSearch } from "react-icons/bs";

// data
import { news } from "../../data/data";

export default function Newsreel({ loginPage, feedsSwitched }) {
  const [newsCount, setNewsCount] = useState(10);
  // set ariable to hold news articles
  const [newsArticle, setNewsArticle] = useState([]);
  // get news articles
  useEffect(() => {
    // url for news API
    const newsURL =
      "https://newsapi.org/v2/everything?" +
      "q=sports&" +
      "apiKey=878d6b3fb383488089f87defc72320c4";

    // fetch news from news API
    const getNews = async () => {
      const response = await axios.get(newsURL);

      // sends response to local storage to prevent multiple refreshes to API server
      localStorage.setItem("articles", JSON.stringify(response.data.articles));
    };
    if (!localStorage.getItem("articles")) {
      console.log("Article does not exist in local storage");
      getNews();
    } else {
      console.log("Article exists in local storage");
      const articles = JSON.parse(localStorage.getItem("articles"));
      setNewsArticle((prev) => articles.slice(0, newsCount));
    }
  }, [newsCount]);

  // function to show search news input field when search icon is clicked
  const showSearchInput = () => {
    document.getElementById("search-input").classList.toggle("active");
  };

  // function to listen to small screen size
  const [smallScreen, setSmallScreen] = useState(false);
  useEffect(() => {
    const windowResizeListener = (window.onresize = () => {
      if (window.innerWidth <= 920) {
        setSmallScreen(true);
      } else {
        setSmallScreen(false);
      }
    });

    return windowResizeListener();
  }, []);

  return (
    <div className="newsreelDiv">
      {/* FeedsSwitched is used to control the visibility of the news navigation only on large screen */}
      {!loginPage && !feedsSwitched && !smallScreen && (
        <div className="news-nav">
          <ul>
            <li className="active">All News</li>
            <li>Sport</li>
            <li>Politics</li>
            <li>Metro</li>
            <li>Entertainment &amp; More</li>
          </ul>
        </div>
      )}

      {feedsSwitched && (
        <div className="newspage-navbar-alt">
          <div className="news-filter">
            <TfiLayoutGrid3Alt />
            <select name="news-filter" id="news-filter">
              <option value="All-news">All Updates</option>
              <option value="All-news">Sports</option>
              <option value="All-news">Politics</option>
              <option value="All-news">Metro</option>
              <option value="All-news">Entertainment & More</option>
            </select>
          </div>
          <div className="news-search">
            <input type="text" id="search-input" placeholder="Search news..." />
            <BsSearch className="news-search-icon" onClick={showSearchInput} />
          </div>
        </div>
      )}
      {newsArticle.map((article) => {
        return <IndividualNews key={article.url} article={article} />;
      })}

      <button
        className="btn-solid"
        onClick={() => setNewsCount((prev) => prev + 10)}
      >
        View More
      </button>
    </div>
  );
}
