import React, { useState, useEffect } from 'react'; 

import { Typography } from 'antd';
import myAPI from '../utils/api';
import CaseList from './CaseList';
import { useParams } from "react-router-dom";

const { Title } = Typography;

export default props => {
  const [cases, setCases] = useState(null);
  const [loading, setLoading] = useState(true);
  const { slug } = useParams();
  const title = slug.replace('-', ' ')

  useEffect(() => {
    const getData = async () => {
      try {
        const caseData = await myAPI.getCasesByEntity(slug);
        console.log(caseData);
        setCases(caseData);
      } catch (e) {
      }
      setLoading(false);
    };

    getData();
  }, [slug]);

  return (
    <>
      <Title level={1}>Entity: {title}</Title>
      <CaseList header={'Cases with Entity'} cases={cases} loading={loading} />
    </>
  );
};