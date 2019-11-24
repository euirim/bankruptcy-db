import React, { useState } from "react";
import { Input } from "antd";
import "antd/lib/input/style";

const { Search } = Input;

const CaseSearchBar = props => {
  const [loading, setLoading] = useState(false);
  const onSearch = query => {
    setLoading(true);

    // do something with query
    props.onSearch(query); 

    setLoading(false);
  };

  return (
    <Search
      className="search-bar"
      placeholder={props.placeholder}
      onSearch={onSearch}
      size="large"
      loading={loading}
    />
  );
};

export default CaseSearchBar;
