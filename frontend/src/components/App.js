import React from 'react';
import Todo from './Todo';
import logo from '../assets/logo.svg';

function App() {
  const greeting = 'Hello world!';
  return (
    <div className="App">
      <h1>{greeting}</h1>
      <Todo id={1} />
      <img src={logo} />
    </div>
  );
}

export default App;
