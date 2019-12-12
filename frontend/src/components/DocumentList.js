import React from 'react';
import { List, Typography, Collapse, Icon, Tag, Descriptions } from 'antd';
import { Link } from 'react-router-dom';

import 'antd/lib/list/style';
import 'antd/lib/tag/style';
import 'antd/lib/descriptions/style';
import './DocumentList.less';

const { Text } = Typography;
const { Panel } = Collapse;

const DocumentMeta = props => {
  const people = props.people
    ? props.people.map(p => (
        <Tag>
          <Link to={`/entities/${p[1]}`}>{p[0]}</Link>
        </Tag>
      ))
    : 'N/A';
  const orgs = props.orgs
    ? props.orgs.map(p => (
        <Tag>
          <Link to={`/entities/${p[1]}`}>{p[0]}</Link>
        </Tag>
      ))
    : 'N/A';

  return (
    <Descriptions bordered>
      <Descriptions.Item label="People">{people}</Descriptions.Item>
      <Descriptions.Item label="Organizations">{orgs}</Descriptions.Item>
    </Descriptions>
  );
};

const DocumentListItem = props => {
  const isSealedTag = (
    <>
      {props.isSealed ? (
        <Tag className="doc-title-tag" color="yellow">
          Sealed
        </Tag>
      ) : null}
    </>
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
      <DocumentMeta
        people={props.people}
        orgs={props.orgs}
        entities={props.entities}
      />
    </List.Item>
  );
};

export default props => {
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
              people={d.people}
              orgs={d.organizations}
            />
          )}
        />
      </Panel>
    </Collapse>
  );
};
