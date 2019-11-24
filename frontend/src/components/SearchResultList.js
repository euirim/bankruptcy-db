import React from "react";
import { List, Typography } from "antd";
import "antd/lib/list/style";
import { prettyDate } from "../utils";

const { Title, Text } = Typography;

const SearchResultItem = props => {
  const dateFiled = prettyDate(props.dateFiled);
  const dateCreated = prettyDate(props.dateCreated);
  return (
    <List.Item>
      <List.Item.Meta
        title={props.name}
        description={dateFiled ? dateFiled : dateCreated}
      />
    </List.Item>
  );
};

const SearchResultList = props => {
  return (
    <div className="search-results">
      <List
        dataSource={props.results ? props.results : []}
        loading={props.loading}
        renderItem={item => (
          <SearchResultItem
            key={item.id}
            name={item.name}
            dateFiled={new Date(item.date_filed)}
            dateCreated={new Date(item.date_created)}
          />
        )}
      />
    </div>
  );
};

export default SearchResultList;
