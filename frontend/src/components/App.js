import React from "react";
import { Layout, Menu, Typography } from "antd";
import "antd/lib/menu/style";
import "antd/lib/layout/style";
import "./App.less";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Home from "./Home";
import About from "./About";
import Search from "./Search";
import Case from "./Case";

const { Header, Content, Footer } = Layout;
const { Title } = Typography;

function App() {
  return (
    <div className="App">
      <Layout className="layout">
        <Router>
          <Header>
            <div className="logo">
              <Title>
                <Link to="/">Bankruptcy Map</Link>
              </Title>
            </div>
            <Menu className="nav" theme="dark" mode="horizontal">
              <Menu.Item key="1" style={{ float: "right", paddingRight: 0 }}>
                <Link to="/about">About</Link>
              </Menu.Item>
            </Menu>
          </Header>
          <Content style={{ padding: "24px 50px" }}>
            <Switch>
              <Route path="/about">
                <About />
              </Route>
              <Route path="/cases/:id">
                <Case />
              </Route>
              <Route path="/search/:queryString">
                <Search />
              </Route>
              <Route path="/">
                <Home />
              </Route>
            </Switch>
          </Content>
          <Footer style={{ textAlign: "center" }}>©2019 Bankruptcy Map</Footer>
        </Router>
      </Layout>
    </div>
  );
}

export default App;
