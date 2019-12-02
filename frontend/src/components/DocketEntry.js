import React, { useState, useEffect } from 'react';
import { List, Typography, Collapse, Icon } from 'antd';

import { prettyDate } from '../utils';
import myAPI from '../utils/api';
import 'antd/lib/list/style';
import './DocketEntry.less';

const { Title } = Typography;
const { Panel } = Collapse;

const DocumentListItem = props => {
  return (
    <List.Item
      key={props.key}
      extra={
        props.preview ? (
          <a href={props.fileUrl}>
            <img width={100} alt="document_preview" src={props.preview} />
          </a>
        ) : null
      }
    >
      <List.Item.Meta
        title={
          props.fileUrl ? <a href={props.fileUrl}>{props.id}</a> : props.id
        }
        description={
          props.description ? props.description : 'Description not available.'
        }
      />
    </List.Item>
  );
};

const DocumentList = props => {
  return (
    <Collapse
      bordered={false}
      expandIcon={({ isActive }) => (
        <Icon type="caret-right" rotate={isActive ? 90 : 0} />
      )}
      destroyInactivePanel
      className="collapse-inset"
    >
      <Panel header="Documents" key="1">
        <List
          dataSource={props.docs}
          itemLayout="vertical"
          renderItem={(d, i) => (
            <DocumentListItem
              key={i}
              fileUrl={d.file_url}
              title={d.id}
              description={d.description}
              preview={d.preview}
            />
          )}
        />
      </Panel>
    </Collapse>
  );
};

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
    <List.Item>
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
