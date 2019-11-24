import React, { useState } from "react";
import { Input } from "antd";
import "antd/lib/input/style";

const { Search } = Input;

const CaseSearchBar = props => {
  const onSearch = query => {
    // do something with query
    props.onSearch(query); 
  };

  return (
    <Search
      className="search-bar"
      placeholder={props.placeholder}
      onSearch={onSearch}
      size="large"
      defaultValue={props.passedQuery}
      loading={props.loading}
    />
  );
};

export default CaseSearchBar;
