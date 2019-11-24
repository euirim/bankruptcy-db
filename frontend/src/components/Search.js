import React, { useState } from "react";
import CaseSearchBar from "./CaseSearchBar";
import axios from 'axios';
import "./Search.less";
import SearchResultList from "./SearchResultList";

const Search = props => {
  const [results, setResults] = useState(null);
  const onSearch = query => {
    // API query
    axios.get(`http://localhost:8000/api/v1/search?q=${query}`)
      .then(res => {
        setResults(res.data);
      })
  };

  return (
    <>
      <div className="search-header">
        <CaseSearchBar className="search-bar" onSearch={onSearch} />
      </div>

      <SearchResultList results={results} />
    </>
  );
};

export default Search;
