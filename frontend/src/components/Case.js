import React, { useState, useEffect } from "react";
import {
  PageHeader,
  Typography,
  Descriptions,
  Button,
  List,
  Card,
  Badge
} from "antd";
import myAPI from "../utils/api";
import { useParams } from "react-router-dom";
import { prettyDate } from "../utils";
import "antd/lib/badge/style";
import "antd/lib/button/style";
import "antd/lib/card/style";
import "antd/lib/descriptions/style";
import "antd/lib/list/style";
import "antd/lib/page-header/style";
import "./Case.less";

const { Title } = Typography;

const CaseHeader = props => {
  const handleNA = val => {
    return val ? val : "N/A";
  };

  console.log(props.name);
  return (
    <PageHeader
      className="case-header"
      ghost
      title={props.name}
      extra={[
        <Button
          href={props.recapUrl}
          type="primary"
          shape="round"
          icon="export"
        >
          View on Recap
        </Button>
      ]}
    >
      <Descriptions bordered size="small">
        <Descriptions.Item label="PACER ID">{props.pacerId}</Descriptions.Item>
        <Descriptions.Item label="RECAP ID">{props.recapId}</Descriptions.Item>
        <Descriptions.Item label="Date Filed">
          {handleNA(prettyDate(props.dateFiled))}
        </Descriptions.Item>
        <Descriptions.Item label="Date Created">
          {handleNA(prettyDate(props.dateCreated))}
        </Descriptions.Item>
        <Descriptions.Item label="Date Terminated">
          {handleNA(prettyDate(props.dateTerminated))}
        </Descriptions.Item>
        <Descriptions.Item label="Date Blocked">
          {handleNA(prettyDate(props.dateBlocked))}
        </Descriptions.Item>
        <Descriptions.Item label="Jurisdiction">
          {handleNA(props.jurisdiction)}
        </Descriptions.Item>
        <Descriptions.Item label="Chapter">
          {handleNA(props.chapter)}
        </Descriptions.Item>
      </Descriptions>
    </PageHeader>
  );
};

const DocketEntry = props => {
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
        title={`Document ${entry.recap_id}`}
        description={
          entry.description ? entry.description : "Description not available."
        }
      />
    </List.Item>
  );
};

const CaseDocket = props => {
  return (
    <Card
      className="caseDocket"
      title={
        <>
          Docket{"  "}
          <Badge
            count={props.docketEntries.length}
            style={{ "background-color": "#1890ff" }}
          />
        </>
      }
    >
      <List
        dataSource={props.docketEntries ? props.docketEntries : []}
        loading={props.loading}
        renderItem={item => <DocketEntry key={item} id={item} />}
      />
    </Card>
  );
};

const Case = () => {
  const [caseItem, setCase] = useState(null);
  const [caseAvailable, setCaseAvailable] = useState(true);
  const [loading, setLoading] = useState(true);
  const { id } = useParams();

  useEffect(() => {
    const getData = async () => {
      try {
        const c = await myAPI.getCase(id);
        setCase(c);
      } catch (e) {
        setCaseAvailable(false);
      }
      setLoading(false);
    };

    getData();
  }, [id]);

  if (!caseAvailable) {
    return <Title level={2}>Case not found.</Title>;
  }

  if (loading) {
    return <Title level={2}>Loading...</Title>;
  }

  return (
    <>
      <CaseHeader
        name={caseItem.name}
        pacerId={caseItem.pacer_id}
        recapId={caseItem.recap_id}
        dateFiled={caseItem.date_filed}
        dateCreated={caseItem.date_created}
        dateTerminated={caseItem.date_terminated}
        dateBlocked={caseItem.date_blocked}
        jurisdiction={caseItem.jurisdiction}
        chapter={caseItem.chapter}
        recapUrl={caseItem.recap_url}
      />
      <CaseDocket docketEntries={caseItem.docket_entries} loading={loading} />
    </>
  );
};

export default Case;
