import React, { useState, useEffect } from 'react';

import myAPI from '../utils/api';
import CaseList from './CaseList';
import './SimilarCases.less';

export default props => {
  const [cases, setCases] = useState(null);
  const [loading, setLoading] = useState(true);

  if (!props.entities && !props.creditors) {
    return <></>;
  }

  useEffect(() => {
    const getData = async () => {
      try {
        const caseData = await myAPI.getSimilarCases(props.caseId);
        setCases(caseData);
      } catch (e) {}
      setLoading(false);
    };

    getData();
  }, [props.caseId]);

  return (
    <CaseList
      className="case-list"
      header={'Possibly Similar Cases'}
      cases={cases}
      loading={loading}
    />
  );
};
