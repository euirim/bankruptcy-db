import React from "react";
import { Row, Col, Typography } from "antd";
import "./Home.less";
import "antd/lib/input/style";
import CaseSearchBar from "./CaseSearchBar";

const { Title, Paragraph } = Typography;

const Home = () => {
  return (
    <>
      <div className="banner">
        <Row type="flex" justify="center">
          <Col>
            <Title className="header" strong>
              Exploring Bankruptcies at Scale
            </Title>
            <CaseSearchBar className="search-bar" />
            <Paragraph className="subtitle">
              Finding <strong>interesting trends</strong> in United States{" "}
              <strong>bankruptcy court documents</strong> using network science
              and state-of-the-art natural language processing.
            </Paragraph>
          </Col>
        </Row>
      </div>
    </>
  );
};

export default Home;
