import React from 'react';

import { List, Typography, Icon } from 'antd';
import 'antd/lib/list/style';
import 'antd/lib/icon/style';
import { prettyDate } from '../utils';
import { Link } from 'react-router-dom';
import './CaseList.less';

const { Text } = Typography;

const CaseListItem = props => {
  const dateFiled = prettyDate(props.dateFiled);
  const dateCreated = prettyDate(props.dateCreated);
  return (
    <List.Item className='case-list-item'>
      <List.Item.Meta
        title={<Link to={`/cases/${props.id}`}>{props.name}</Link>}
        description={`PACER: ${props.pacerId}`}
      />
      <>
        <Icon type="calendar" /> {dateFiled ? dateFiled : dateCreated}
      </>
    </List.Item>
  );
};

export default props => {
  return (
    <List
      className="case-list"
      bordered
      itemLayout="vertical"
      header={
        props.header ? (
          <Text className="case-list-header">{props.header}</Text>
        ) : (
          false
        )
      }
      dataSource={props.cases ? props.cases : []}
      loading={props.loading}
      renderItem={item => (
        <CaseListItem
          key={item.id}
          id={item.id}
          name={item.name}
          dateFiled={item.date_filed}
          dateCreated={item.date_created}
          pacerId={item.pacer_id}
        />
      )}
    />
  );
};
