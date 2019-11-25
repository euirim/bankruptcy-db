import React, { useState, useEffect } from "react";
import CaseSearchBar from "./CaseSearchBar";
import axios from "axios";
import "./Search.less";
import SearchResultList from "./SearchResultList";
import { useParams, useHistory } from "react-router-dom";

const Search = props => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const { queryString } = useParams();
  const history = useHistory();

  useEffect(() => {
    setLoading(true);
    axios
      .get(
        process.env.NODE_ENV === "development"
          ? `http://localhost:8000/api/v1/search?q=${queryString}`
          : `search?q=${queryString}`
      )
      .then(res => {
        setResults(res.data);
        setLoading(false);
      });
  }, [queryString]);

  const onSearch = query => {
    history.push(`/search/${encodeURI(query)}`);
  };

  return (
    <>
      <div className="search-header">
        <CaseSearchBar
          className="search-bar"
          onSearch={onSearch}
          loading={loading}
          passedQuery={queryString}
        />
      </div>

      <SearchResultList results={results} loading={loading} />
    </>
  );
};

export default Search;
