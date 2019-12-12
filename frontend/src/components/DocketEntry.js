import React, { useState, useEffect } from 'react';
import { List, Typography } from 'antd';

import { prettyDate } from '../utils';
import myAPI from '../utils/api';
import DocumentList from './DocumentList';
import 'antd/lib/list/style';
import 'antd/lib/tag/style';
import './DocketEntry.less';

const { Title } = Typography;

export default props => {
  const [entry, setEntry] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getData = async () => {
      try {
        const result = await myAPI.getDocketEntry(props.id);
        console.log(result);
        setEntry(result);
      } catch (e) {
        console.log(e);
      }
      setLoading(false);
    };
    getData();
  }, [props.id]);

  if (!entry) {
    return <Title level={3}>Loading...</Title>;
  }

  return (
    <List.Item className="docket-entry-item">
      <List.Item.Meta
        title={prettyDate(entry.date_filed)}
        description={
          entry.description ? entry.description : 'Description not available.'
        }
      />
      <DocumentList docs={entry.documents} />
    </List.Item>
  );
};
