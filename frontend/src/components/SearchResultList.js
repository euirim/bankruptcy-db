import React from 'react';

import CaseList from './CaseList';

const SearchResultList = props => {
  return (
    <div className="search-results">
      <CaseList cases={props.results} loading={props.loading} header={`${props.results ? props.results.length : 0} Case Results`} />
    </div>
  );
};

export default SearchResultList;
