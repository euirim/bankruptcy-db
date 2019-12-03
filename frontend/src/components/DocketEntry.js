import React, { useState, useEffect } from 'react';
import { List, Typography, Collapse, Icon, Tag } from 'antd';

import { prettyDate } from '../utils';
import myAPI from '../utils/api';
import 'antd/lib/list/style';
import 'antd/lib/tag/style';
import './DocketEntry.less';

const { Text, Title } = Typography;
const { Panel } = Collapse;

const DocumentListItem = props => {
  const isSealedTag = (
    <>{props.isSealed ? <Tag className="doc-title-tag" color="yellow">Sealed</Tag> : null}</>
  );
  return (
    <List.Item
      className="doc-list-item"
      key={props.key}
      extra={
        props.preview ? (
          <a href={props.fileUrl} target="_blank">
            <div className="doc-preview">
              <img width={150} alt="document_preview" src={props.preview} />
            </div>
          </a>
        ) : null
      }
    >
      <List.Item.Meta
        title={
          props.fileUrl ? (
            <>
              <a href={props.fileUrl} target="_blank">
                PACER: {props.title ? props.title : 'Unknown'}
              </a>
              {isSealedTag}
            </>
          ) : (
            <>
              {`PACER: ${props.title ? props.title : 'Unknown'}`}
              <Tag className="doc-title-tag" color="red">
                Unavailable
              </Tag>
              {isSealedTag}
            </>
          )
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
      <Panel
        header={
          <Text className="docs-panel-header-title">
            Documents ({props.docs.length})
          </Text>
        }
        key="1"
      >
        <List
          className="doc-list"
          dataSource={props.docs}
          bordered
          itemLayout="vertical"
          renderItem={(d, i) => (
            <DocumentListItem
              key={i}
              fileUrl={d.file_url}
              title={d.pacer_id}
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
