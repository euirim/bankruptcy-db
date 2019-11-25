import React, { useState, useEffect } from "react";
import { PageHeader, Typography, Descriptions, Button } from "antd";
import myAPI from "../utils/api";
import { useParams } from "react-router-dom";
import "antd/lib/button/style";
import "antd/lib/descriptions/style";
import "antd/lib/page-header/style";
import "./Case.less";

const { Title } = Typography;

const CaseHeader = props => {
  const handleNA = val => {
    return val ? val : "N/A";
  };

  console.log(props.linkToOriginal);
  return (
    <PageHeader
      className="case-header"
      ghost
      title={props.name}
      extra={[
        <Button
          href={props.linkToOriginal}
          type="primary"
          shape="round"
          icon="download"
        >
          Download Data
        </Button>
      ]}
    >
      <Descriptions bordered size="small">
        <Descriptions.Item label="PACER ID">{props.pacerId}</Descriptions.Item>
        <Descriptions.Item label="RECAP ID">{props.recapId}</Descriptions.Item>
        <Descriptions.Item label="Date Filed">
          {handleNA(props.dateFiled)}
        </Descriptions.Item>
        <Descriptions.Item label="Date Created">
          {handleNA(props.dateCreated)}
        </Descriptions.Item>
        <Descriptions.Item label="Date Terminated">
          {handleNA(props.dateTerminated)}
        </Descriptions.Item>
        <Descriptions.Item label="Date Blocked">
          {handleNA(props.dateBlocked)}
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

const Case = () => {
  const [caseItem, setCase] = useState(null);
  const [caseAvailable, setCaseAvailable] = useState(true);
  const [loading, setLoading] = useState(true);
  const { id } = useParams();

  useEffect(() => {
    const getData = async () => {
      try {
        const c = await myAPI.getCase(id);
        console.log(c);
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

  return (
    <>
      {loading ? (
        <Title level={2}>Loading...</Title>
      ) : (
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
          linkToOriginal={null}
        />
      )}
    </>
  );
};

export default Case;
