import React, { useState, useEffect } from 'react';
import {
  PageHeader,
  Typography,
  Descriptions,
  Button,
  List,
  Card,
  Badge,
  Alert,
  Tag,
} from 'antd';
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';

import myAPI from '../utils/api';
import DocketEntry from './DocketEntry';
import { prettyDate } from '../utils';
import 'antd/lib/alert/style';
import 'antd/lib/badge/style';
import 'antd/lib/button/style';
import 'antd/lib/card/style';
import 'antd/lib/descriptions/style';
import 'antd/lib/list/style';
import 'antd/lib/page-header/style';
import 'antd/lib/tag/style';
import './Case.less';

const { Title } = Typography;

const CaseHeader = props => {
  const handleNA = val => {
    return val ? val : 'N/A';
  };
  const creditors = props.creditors
    ? props.creditors.map(p => (
        <Tag color='green'>
          <Link to={`/entities/${p[1]}`}>{p[0]}</Link>
        </Tag>
      ))
    : 'N/A';

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
          target="_blank"
        >
          View on Recap
        </Button>,
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
        <Descriptions.Item label="Creditors">
          {handleNA(creditors)}
        </Descriptions.Item>
      </Descriptions>
    </PageHeader>
  );
};

const CaseDocket = props => {
  return (
    <Card
      className="caseDocket"
      title={
        <>
          Docket{'  '}
          <Badge
            count={props.docketEntries.length}
            style={{ 'background-color': '#1890ff' }}
          />
        </>
      }
    >
      <Alert
        className="docket-alert"
        message="Docket May Be Incomplete"
        description="Please reference the original case on PACER to verify any conclusions."
        type="warning"
        showIcon
      />
      <List
        dataSource={props.docketEntries ? props.docketEntries : []}
        loading={props.loading}
        renderItem={item => <DocketEntry key={item} id={item} />}
        itemLayout="vertical"
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
        creditors={caseItem.creditors}
      />
      <CaseDocket
        docketEntries={caseItem.docket_entries.slice(0, 30)}
        loading={loading}
      />
    </>
  );
};

export default Case;
