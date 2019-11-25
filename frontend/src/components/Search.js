import React, { useState, useEffect } from "react";
import CaseSearchBar from "./CaseSearchBar";
import "./Search.less";
import SearchResultList from "./SearchResultList";
import { useParams, useHistory } from "react-router-dom";
import myAPI from "../utils/api";

const Search = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const { queryString } = useParams();
  const history = useHistory();

  useEffect(() => {
    const getData = async () => {
      setLoading(true);
      try {
        const res = await myAPI.search(queryString);
        setResults(res);
      } catch (e) {
        console.log(e);
      }
      setLoading(false);
    };
    getData();
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
