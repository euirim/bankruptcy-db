import React from "react";
import { Layout, Menu } from "antd";
import "antd/lib/menu/style";
import "antd/lib/layout/style";
import "./App.less";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Home from "./Home";
import About from "./About";

const { Header, Content, Footer } = Layout;

function App() {
  return (
    <div className="App">
      <Layout className="layout">
        <Router>
          <Header>
            <div className="logo">
              <h1>
                <Link to="/">Bankruptcy Map</Link>
              </h1>
            </div>
            <Menu
              className="nav"
              theme="dark"
              mode="horizontal"
            >
              <Menu.Item key="1">
                <Link to="/about">About</Link>
              </Menu.Item>
            </Menu>
          </Header>
          <Content style={{ padding: "0 50px" }}>
            <Switch>
              <Route path="/">
                <Home />
              </Route>
              <Route path="/about">
                <About />
              </Route>
            </Switch>
          </Content>
          <Footer style={{ textAlign: "center" }}>Bankruptcy Map ©2019</Footer>
        </Router>
      </Layout>
    </div>
  );
}

export default App;
